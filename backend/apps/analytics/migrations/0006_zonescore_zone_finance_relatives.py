from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_analyticsresult_bridge_analysis_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zonescore',
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
