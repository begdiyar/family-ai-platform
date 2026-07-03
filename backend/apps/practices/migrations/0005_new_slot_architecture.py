import uuid
import django.db.models.deletion
from django.db import migrations, models


# ── Data migration ────────────────────────────────────────────────────────────

def migrate_forward(apps, schema_editor):
    Practice = apps.get_model('practices', 'Practice')
    DailyAssignment = apps.get_model('practices', 'DailyAssignment')
    AssignmentSlot = apps.get_model('practices', 'AssignmentSlot')

    # 1. Remap old categories that were renamed or merged
    CAT_REMAP = {
        'emotional': 'intimacy',
        'support':   'trust',
        'conflict':  'communication',
        'goals':     'gratitude',
        'parenting': 'children',
    }
    for old_cat, new_cat in CAT_REMAP.items():
        Practice.objects.filter(category=old_cat).update(category=new_cat)

    # 2. Copy practice_type → slot_type before removing practice_type
    TYPE_TO_SLOT = {
        'question': 'conversation',
        'action':   'gesture',
        'exercise': 'activity',
    }
    for practice_type, slot_type in TYPE_TO_SLOT.items():
        Practice.objects.filter(practice_type=practice_type).update(slot_type=slot_type)
    # Any practice with an unknown type gets 'main'
    Practice.objects.exclude(
        practice_type__in=list(TYPE_TO_SLOT.keys())
    ).update(slot_type='main')

    # 3. Migrate existing DailyAssignment FK slots → AssignmentSlot rows
    FIELD_MAP = [
        ('question_id', 'question_completed', 'main'),
        ('action_id',   'action_completed',   'gesture'),
        ('exercise_id', 'exercise_completed', 'activity'),
    ]
    slots_to_create = []
    for assignment in DailyAssignment.objects.all():
        for pk_field, done_field, slot_type in FIELD_MAP:
            practice_id = getattr(assignment, pk_field, None)
            completed   = getattr(assignment, done_field, False)
            slots_to_create.append(
                AssignmentSlot(
                    id=uuid.uuid4(),
                    assignment=assignment,
                    slot_type=slot_type,
                    practice_id=practice_id,
                    completed=completed,
                )
            )
    if slots_to_create:
        AssignmentSlot.objects.bulk_create(slots_to_create, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0004_practice_i18n'),
    ]

    operations = [
        # ── Practice: add slot_type ───────────────────────────────────────────
        migrations.AddField(
            model_name='practice',
            name='slot_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('main',         'Практика дня'),
                    ('conversation', 'Тема разговора'),
                    ('gesture',      'Маленький жест любви'),
                    ('activity',     'Семейная активность'),
                    ('growth',       'Рекомендация для роста'),
                ],
                default='main',
                db_index=True,
            ),
            preserve_default=False,
        ),

        # ── Practice: add tags ────────────────────────────────────────────────
        migrations.AddField(
            model_name='practice',
            name='tags',
            field=models.JSONField(default=list, blank=True),
        ),

        # ── AssignmentSlot model ──────────────────────────────────────────────
        migrations.CreateModel(
            name='AssignmentSlot',
            fields=[
                ('id',           models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at',   models.DateTimeField(auto_now_add=True)),
                ('updated_at',   models.DateTimeField(auto_now=True)),
                ('assignment',   models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='slots',
                    to='practices.dailyassignment',
                )),
                ('slot_type',    models.CharField(
                    max_length=20,
                    choices=[
                        ('main',         'Практика дня'),
                        ('conversation', 'Тема разговора'),
                        ('gesture',      'Маленький жест любви'),
                        ('activity',     'Семейная активность'),
                        ('growth',       'Рекомендация для роста'),
                    ],
                    db_index=True,
                )),
                ('practice',     models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='slots',
                    to='practices.practice',
                )),
                ('completed',    models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={'db_table': 'assignment_slots'},
        ),
        migrations.AlterUniqueTogether(
            name='assignmentslot',
            unique_together={('assignment', 'slot_type')},
        ),

        # ── Data migration ────────────────────────────────────────────────────
        migrations.RunPython(migrate_forward, migrations.RunPython.noop),

        # ── Practice: remove old practice_type ───────────────────────────────
        migrations.RemoveField(model_name='practice', name='practice_type'),

        # ── DailyAssignment: remove old FK slot fields ───────────────────────
        migrations.RemoveField(model_name='dailyassignment', name='question'),
        migrations.RemoveField(model_name='dailyassignment', name='action'),
        migrations.RemoveField(model_name='dailyassignment', name='exercise'),
        migrations.RemoveField(model_name='dailyassignment', name='question_completed'),
        migrations.RemoveField(model_name='dailyassignment', name='action_completed'),
        migrations.RemoveField(model_name='dailyassignment', name='exercise_completed'),
    ]
