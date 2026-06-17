from django.db import models
from shared.models import BaseModel


class AIConversation(BaseModel):
    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='ai_conversations')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='ai_conversations')
    title = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'ai_conversations'
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['couple', 'user']),
        ]

    def __str__(self):
        return f"Conv({self.user.first_name}, {self.title or 'без названия'})"


class AIMessage(BaseModel):
    ROLE_USER = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLE_SYSTEM = 'system'
    ROLE_CHOICES = [
        (ROLE_USER, 'Пользователь'),
        (ROLE_ASSISTANT, 'Ассистент'),
        (ROLE_SYSTEM, 'Система'),
    ]

    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    tokens_used = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ai_messages'
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]

    def __str__(self):
        return f"Message({self.role}, {self.content[:40]})"
