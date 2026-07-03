from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_extended_profile'),
    ]

    operations = [
        # 1. Add phone as nullable first so existing rows get NULL
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        # 2. Populate phone from email for existing users
        migrations.RunSQL(
            "UPDATE users SET phone = CONCAT('t', LEFT(REPLACE(id::text, '-', ''), 14)) WHERE phone IS NULL",
            reverse_sql="UPDATE users SET phone = NULL",
        ),
        # 3. Make phone required and unique
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, unique=True),
        ),
        # 4. Make email optional
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, null=True, blank=True),
        ),
    ]
