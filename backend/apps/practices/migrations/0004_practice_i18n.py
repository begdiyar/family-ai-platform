from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0003_practices_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
