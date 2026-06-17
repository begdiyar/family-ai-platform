from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0002_academy_i18n'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='training',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
