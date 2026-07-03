from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0006_rename_diagnostic_sessions_couple_user_level_idx_diagnostic__couple__bba3f3_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
