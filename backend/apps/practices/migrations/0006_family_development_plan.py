import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0005_new_slot_architecture'),
        ('couples', '0003_couple_children_count_couple_has_children_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDevelopmentPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('couple', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='development_plan',
                    to='couples.couple',
                )),
                ('priority_zone',  models.CharField(blank=True, default='', max_length=30)),
                ('secondary_zone', models.CharField(blank=True, default='', max_length=30)),
                ('tertiary_zone',  models.CharField(blank=True, default='', max_length=30)),
                ('current_level',  models.PositiveSmallIntegerField(default=1)),
                ('current_stage',  models.PositiveSmallIntegerField(default=1)),
                ('total_completed', models.PositiveIntegerField(default=0)),
                ('last_diagnostic_at', models.DateTimeField(blank=True, null=True)),
                ('next_diagnostic_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'family_development_plans',
            },
        ),
    ]
