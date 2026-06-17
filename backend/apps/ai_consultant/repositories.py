from typing import List, Optional
from .models import AIConversation, AIMessage
from apps.users.models import User
from apps.couples.models import Couple


class AIConversationRepository:
    @staticmethod
    def create(couple: Couple, user: User, title: str = None) -> AIConversation:
        return AIConversation.objects.create(couple=couple, user=user, title=title)

    @staticmethod
    def list_for_user(user: User) -> List[AIConversation]:
        return list(
            AIConversation.objects
            .filter(user=user)
            .annotate_messages_count()
            .order_by('-updated_at')
        ) if hasattr(AIConversation.objects, 'annotate_messages_count') else list(
            AIConversation.objects.filter(user=user).order_by('-updated_at')
        )

    @staticmethod
    def get_by_id(conv_id, user: User) -> Optional[AIConversation]:
        return AIConversation.objects.filter(id=conv_id, user=user).first()


class AIMessageRepository:
    @staticmethod
    def create(conversation: AIConversation, role: str, content: str, tokens_used: int = None) -> AIMessage:
        return AIMessage.objects.create(
            conversation=conversation,
            role=role,
            content=content,
            tokens_used=tokens_used,
        )

    @staticmethod
    def get_recent(conversation: AIConversation, limit: int = 20) -> List[AIMessage]:
        messages = list(
            AIMessage.objects
            .filter(conversation=conversation)
            .exclude(role=AIMessage.ROLE_SYSTEM)
            .order_by('-created_at')[:limit]
        )
        return list(reversed(messages))

    @staticmethod
    def list_for_conversation(conversation: AIConversation, limit: int = 20, before_id=None):
        qs = AIMessage.objects.filter(conversation=conversation).exclude(role=AIMessage.ROLE_SYSTEM)
        if before_id:
            pivot = AIMessage.objects.filter(id=before_id).first()
            if pivot:
                qs = qs.filter(created_at__lt=pivot.created_at)
        messages = list(qs.order_by('-created_at')[:limit])
        return list(reversed(messages)), qs.count() > limit
