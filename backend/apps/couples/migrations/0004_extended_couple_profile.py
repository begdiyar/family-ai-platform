import uuid
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('couples', '0003_couple_children_count_couple_has_children_and_more'),
    ]

    operations = [
        # ── FamilyValue lookup table ──────────────────────────────────────────
        migrations.CreateModel(
            name='FamilyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.CharField(max_length=30, unique=True)),
                ('label_ru', models.CharField(max_length=100)),
            ],
            options={'db_table': 'family_values', 'ordering': ['label_ru']},
        ),

        # ── New Couple fields ─────────────────────────────────────────────────
        migrations.AddField(
            model_name='couple',
            name='relationship_status',
            field=models.CharField(
                blank=True, default='',
                choices=[
                    ('dating', 'Встречаемся'), ('engaged', 'Помолвлены'),
                    ('cohabitating', 'Живём вместе'), ('married', 'Женаты/замужем'),
                    ('separated', 'Живём раздельно'),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='couple',
            name='relationship_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='couple',
            name='marriage_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='couple',
            name='lives_with_parents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='couple',
            name='relatives_influence_level',
            field=models.PositiveSmallIntegerField(
                blank=True, null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AddField(
            model_name='couple',
            name='religious_traditions_importance',
            field=models.PositiveSmallIntegerField(
                blank=True, null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AddField(
            model_name='couple',
            name='family_values',
            field=models.ManyToManyField(
                blank=True, related_name='couples', to='couples.familyvalue',
            ),
        ),

        # ── Child model ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(
                    blank=True, default='',
                    choices=[('male', 'Мальчик'), ('female', 'Девочка')],
                    max_length=10,
                )),
                ('couple', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='children',
                    to='couples.couple',
                )),
            ],
            options={'db_table': 'children', 'ordering': ['birth_date']},
        ),
    ]
