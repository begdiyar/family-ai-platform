from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='programday',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='academymicropractice',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
