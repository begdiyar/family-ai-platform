from django.db import models
from shared.models import BaseModel


class ConflictSession(BaseModel):
    STATUS_COLLECTING = 'collecting'
    STATUS_ANALYZING = 'analyzing'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES = [
        (STATUS_COLLECTING, 'Сбор описаний'),
        (STATUS_ANALYZING, 'Анализ'),
        (STATUS_COMPLETE, 'Завершён'),
    ]

    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='conflict_sessions')
    title = models.CharField(max_length=300, default='Конфликт')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_COLLECTING)
    ai_analysis = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'conflict_sessions'
        indexes = [models.Index(fields=['couple', '-created_at'])]

    def __str__(self):
        return f"ConflictSession({self.title}, {self.status})"

    def both_submitted(self):
        return self.entries.count() >= 2

    def get_entry(self, user):
        return self.entries.filter(user=user).first()


class ConflictEntry(BaseModel):
    session = models.ForeignKey(ConflictSession, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    description = models.TextField()
    feelings = models.TextField(blank=True, default='')
    desired_outcome = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'conflict_entries'
        unique_together = [['session', 'user']]

    def __str__(self):
        return f"ConflictEntry({self.user.first_name})"
