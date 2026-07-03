import logging

from django.db import migrations

logger = logging.getLogger(__name__)


def migrate_coach_to_ai(apps, schema_editor):
    """
    Copy CoachConversation + CoachMessage rows into AIConversation + AIMessage.
    UUIDs are preserved so existing conversation_id references keep working.
    Skips rows whose UUID already exists in ai_conversations (idempotent).
    """
    CoachConversation = apps.get_model('ai', 'CoachConversation')
    CoachMessage      = apps.get_model('ai', 'CoachMessage')
    AIConversation    = apps.get_model('ai_consultant', 'AIConversation')
    AIMessage         = apps.get_model('ai_consultant', 'AIMessage')

    existing_ids = set(AIConversation.objects.values_list('id', flat=True))
    conv_count   = 0
    msg_count    = 0

    for coach_conv in CoachConversation.objects.select_related('user', 'couple').all():
        if coach_conv.id in existing_ids:
            continue

        ai_conv = AIConversation(
            id          = coach_conv.id,
            user        = coach_conv.user,
            couple      = coach_conv.couple,
            dialog_type = coach_conv.dialog_type,   # 'coach' or 'mediator' — same strings
            title       = coach_conv.title,
        )
        ai_conv.save()
        existing_ids.add(ai_conv.id)
        conv_count += 1

        for msg in CoachMessage.objects.filter(conversation=coach_conv).order_by('created_at'):
            AIMessage.objects.create(
                id           = msg.id,
                conversation = ai_conv,
                role         = msg.role,
                content      = msg.content,
                tokens_used  = msg.tokens_used if msg.tokens_used else None,
            )
            msg_count += 1

    logger.info(
        'data_migrate_coach_conversations: перенесено %d диалогов, %d сообщений',
        conv_count, msg_count,
    )
    print(f'\n  ✓ Перенесено диалогов:   {conv_count}')
    print(f'  ✓ Перенесено сообщений: {msg_count}')


def reverse_migrate(apps, schema_editor):
    """
    Remove AIConversation rows that originated from CoachConversation.
    Identifies them by dialog_type in ('coach', 'mediator').
    AIMessages are deleted via CASCADE.
    """
    CoachConversation = apps.get_model('ai', 'CoachConversation')
    AIConversation    = apps.get_model('ai_consultant', 'AIConversation')

    coach_ids = set(CoachConversation.objects.values_list('id', flat=True))
    deleted, _ = AIConversation.objects.filter(
        id__in         = coach_ids,
        dialog_type__in = ('coach', 'mediator'),
    ).delete()
    print(f'\n  ↩ Отменено: удалено {deleted} AIConversation записей')


class Migration(migrations.Migration):

    dependencies = [
        ('ai_consultant', '0005_aiconversation_dialog_type_couple_nullable'),
        ('ai', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_coach_to_ai, reverse_migrate),
    ]
