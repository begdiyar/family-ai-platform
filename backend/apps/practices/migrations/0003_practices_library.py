import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0002_dailypractice_i18n'),
        ('couples', '0003_couple_children_count_couple_has_children_and_more'),
    ]

    operations = [
        # ── Remove old AI-driven tables ──────────────────────────────────────────
        migrations.DeleteModel('PracticeCompletion'),
        migrations.DeleteModel('DailyPractice'),

        # ── Practice library ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('instructions', models.TextField()),
                ('category', models.CharField(
                    db_index=True, max_length=30,
                    choices=[
                        ('communication', 'Коммуникация'),
                        ('trust',         'Доверие'),
                        ('conflict',      'Конфликты'),
                        ('emotional',     'Эмоциональная близость'),
                        ('gratitude',     'Благодарность'),
                        ('support',       'Поддержка'),
                        ('goals',         'Совместные цели'),
                        ('finances',      'Финансы'),
                        ('romance',       'Романтика'),
                        ('parenting',     'Родительство'),
                    ],
                )),
                ('practice_type', models.CharField(
                    db_index=True, max_length=20,
                    choices=[
                        ('question', 'Вопрос дня'),
                        ('action',   'Действие'),
                        ('exercise', 'Упражнение'),
                    ],
                )),
                ('difficulty', models.CharField(
                    max_length=20, default='easy',
                    choices=[('easy', 'Лёгкий'), ('medium', 'Средний'), ('hard', 'Сложный')],
                )),
                ('duration_minutes', models.PositiveSmallIntegerField(default=10)),
                ('is_active', models.BooleanField(default=True, db_index=True)),
            ],
            options={'db_table': 'practices', 'ordering': ['category', 'difficulty', 'title']},
        ),

        # ── Daily assignment (replaces DailyPractice) ────────────────────────────
        migrations.CreateModel(
            name='DailyAssignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('question_completed', models.BooleanField(default=False)),
                ('action_completed',   models.BooleanField(default=False)),
                ('exercise_completed', models.BooleanField(default=False)),
                ('categories_used',    models.JSONField(default=list, blank=True)),
                ('couple', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='daily_assignments',
                    to='couples.couple',
                )),
                ('question', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='as_question',
                    to='practices.practice',
                )),
                ('action', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='as_action',
                    to='practices.practice',
                )),
                ('exercise', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='as_exercise',
                    to='practices.practice',
                )),
            ],
            options={'db_table': 'daily_assignments'},
        ),
        migrations.AddIndex(
            model_name='dailyassignment',
            index=models.Index(fields=['couple', '-date'], name='daily_assign_couple_date_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='dailyassignment',
            unique_together={('couple', 'date')},
        ),
    ]
