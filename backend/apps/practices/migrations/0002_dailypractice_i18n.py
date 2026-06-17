from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailypractice',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
