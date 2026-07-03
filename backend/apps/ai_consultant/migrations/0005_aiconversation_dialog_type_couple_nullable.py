import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_consultant', '0004_alter_aimessage_tokens_used'),
        ('couples', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiconversation',
            name='dialog_type',
            field=models.CharField(
                choices=[
                    ('chat',     'Чат-консультант'),
                    ('coach',    'Коуч'),
                    ('mediator', 'Медиатор'),
                ],
                default='chat',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='aiconversation',
            name='couple',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ai_conversations',
                to='couples.couple',
            ),
        ),
        migrations.AddIndex(
            model_name='aiconversation',
            index=models.Index(
                fields=['dialog_type', 'user'],
                name='ai_conversa_dialog__type_idx',
            ),
        ),
    ]
