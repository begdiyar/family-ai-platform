from django.db import models
from shared.models import BaseModel


class CoachConversation(BaseModel):
    TYPE_COACH    = 'coach'
    TYPE_MEDIATOR = 'mediator'
    DIALOG_TYPES  = [
        (TYPE_COACH,    'Консультант'),
        (TYPE_MEDIATOR, 'Медиатор'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='coach_conversations',
    )
    couple = models.ForeignKey(
        'couples.Couple',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='coach_conversations',
    )
    dialog_type = models.CharField(
        max_length=20, choices=DIALOG_TYPES, default=TYPE_COACH,
    )
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'ai_coach_conversations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['couple', 'dialog_type']),
        ]

    def __str__(self):
        return f'{self.user.first_name} · {self.dialog_type} · {self.created_at:%Y-%m-%d}'


class CoachMessage(BaseModel):
    ROLE_SYSTEM    = 'system'
    ROLE_USER      = 'user'
    ROLE_ASSISTANT = 'assistant'
    ROLES = [
        (ROLE_SYSTEM,    'System'),
        (ROLE_USER,      'User'),
        (ROLE_ASSISTANT, 'Assistant'),
    ]

    conversation = models.ForeignKey(
        CoachConversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role        = models.CharField(max_length=20, choices=ROLES)
    content     = models.TextField()
    tokens_used = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'ai_coach_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]

    def __str__(self):
        return f'{self.role}: {self.content[:60]}'
