import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0002_initial'),
        ('couples', '0003_couple_children_count_couple_has_children_and_more'),
    ]

    operations = [
        # 1. Add level_number to Question
        migrations.AddField(
            model_name='question',
            name='level_number',
            field=models.SmallIntegerField(default=1),
        ),
        # 2. Update Question index
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['level_number', 'zone', 'order_index']},
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['level_number', 'is_active'], name='questions_level_active_idx'),
        ),

        # 3. Add level_number to DiagnosticSession
        migrations.AddField(
            model_name='diagnosticsession',
            name='level_number',
            field=models.SmallIntegerField(default=1),
        ),
        # 4. Remove old unique_together on DiagnosticSession
        migrations.AlterUniqueTogether(
            name='diagnosticsession',
            unique_together=set(),
        ),
        # 5. Add new unique_together
        migrations.AlterUniqueTogether(
            name='diagnosticsession',
            unique_together={('couple', 'user', 'level_number')},
        ),
        # 6. Rename table to diagnostic_sessions (was diagnostic_sessions already in db_table)
        migrations.AlterModelTable(
            name='diagnosticsession',
            table='diagnostic_sessions',
        ),

        # 7. Create FamilyJourney
        migrations.CreateModel(
            name='FamilyJourney',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('max_unlocked_level', models.SmallIntegerField(default=1)),
                ('last_completed_level', models.SmallIntegerField(default=0)),
                ('couple', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='journey',
                    to='couples.couple',
                )),
            ],
            options={'db_table': 'family_journeys'},
        ),

        # 8. Create LevelProgress
        migrations.CreateModel(
            name='LevelProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level_number', models.SmallIntegerField()),
                ('partner_a_done', models.BooleanField(default=False)),
                ('partner_b_done', models.BooleanField(default=False)),
                ('both_diagnosed_at', models.DateTimeField(blank=True, null=True)),
                ('practices_done_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('journey', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='level_progress',
                    to='diagnostics.familyjourney',
                )),
            ],
            options={
                'db_table': 'level_progress',
                'ordering': ['level_number'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='levelprogress',
            unique_together={('journey', 'level_number')},
        ),

        # 9. Data migration: assign level_number to existing questions by zone
        migrations.RunSQL(
            sql="""
                UPDATE questions SET level_number = 2 WHERE zone = 'communication';
                UPDATE questions SET level_number = 3 WHERE zone = 'trust';
                UPDATE questions SET level_number = 4 WHERE zone = 'intimacy';
                UPDATE questions SET level_number = 5 WHERE zone = 'conflict';
                UPDATE questions SET level_number = 10 WHERE zone = 'values';
                UPDATE questions SET level_number = 10 WHERE zone = 'future';
            """,
            reverse_sql="""
                UPDATE questions SET level_number = 1;
            """,
        ),
    ]
