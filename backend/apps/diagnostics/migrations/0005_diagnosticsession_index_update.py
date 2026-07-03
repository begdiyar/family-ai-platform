from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0004_question_zone_finance_relatives'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='diagnosticsession',
            name='diagnostic__couple__183dba_idx',
        ),
        migrations.AddIndex(
            model_name='diagnosticsession',
            index=models.Index(
                fields=['couple', 'user', 'level_number'],
                name='diagnostic_sessions_couple_user_level_idx',
            ),
        ),
    ]
