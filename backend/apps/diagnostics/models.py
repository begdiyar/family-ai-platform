from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from shared.models import BaseModel


class Question(BaseModel):
    ZONE_COMMUNICATION = 'communication'
    ZONE_TRUST = 'trust'
    ZONE_INTIMACY = 'intimacy'
    ZONE_CONFLICT = 'conflict'
    ZONE_VALUES = 'values'
    ZONE_FUTURE = 'future'
    ZONE_CHOICES = [
        (ZONE_COMMUNICATION, 'Коммуникация'),
        (ZONE_TRUST, 'Доверие'),
        (ZONE_INTIMACY, 'Близость'),
        (ZONE_CONFLICT, 'Конфликты'),
        (ZONE_VALUES, 'Ценности'),
        (ZONE_FUTURE, 'Будущее'),
    ]

    TYPE_SCALE = 'scale'
    TYPE_CHOICE = 'choice'
    TYPE_TEXT = 'text'
    TYPE_CHOICES = [
        (TYPE_SCALE, 'Шкала 1-5'),
        (TYPE_CHOICE, 'Выбор варианта'),
        (TYPE_TEXT, 'Текст'),
    ]

    zone = models.CharField(max_length=30, choices=ZONE_CHOICES)
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SCALE)
    options = models.JSONField(null=True, blank=True)
    order_index = models.SmallIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'questions'
        ordering = ['zone', 'order_index']
        indexes = [
            models.Index(fields=['zone', 'is_active']),
        ]

    def __str__(self):
        return f"[{self.zone}] {self.text[:60]}"


class DiagnosticSession(BaseModel):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_ABANDONED = 'abandoned'
    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_COMPLETED, 'Завершена'),
        (STATUS_ABANDONED, 'Брошена'),
    ]

    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'diagnostic_sessions'
        unique_together = [['couple', 'user']]
        indexes = [
            models.Index(fields=['couple', 'user']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Session({self.user.first_name}, status={self.status})"


class Answer(BaseModel):
    session = models.ForeignKey(DiagnosticSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    value_scale = models.SmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value_choice = models.CharField(max_length=100, null=True, blank=True)
    value_text = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'answers'
        unique_together = [['session', 'question']]
        indexes = [
            models.Index(fields=['session']),
        ]
