from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0003_diagnostic_levels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='zone',
            field=models.CharField(
                max_length=30,
                choices=[
                    ('communication', 'Коммуникация'),
                    ('trust', 'Доверие'),
                    ('intimacy', 'Близость'),
                    ('conflict', 'Конфликты'),
                    ('values', 'Ценности'),
                    ('finance', 'Финансы'),
                    ('relatives', 'Родственники'),
                    ('future', 'Будущее'),
                ],
            ),
        ),
    ]
