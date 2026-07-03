from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0007_alter_practice_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyassignment',
            name='is_ai_generated',
            field=models.BooleanField(default=False),
        ),
    ]
