from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_type',
            field=models.CharField(
                max_length=30,
                choices=[
                    ('diagnostic', 'Диагностика'),
                    ('progress', 'Прогресс'),
                    ('monthly', 'Ежемесячный'),
                ],
            ),
        ),
    ]
