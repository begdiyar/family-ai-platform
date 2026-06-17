from django.db import models
from shared.models import BaseModel


class Report(BaseModel):
    TYPE_DIAGNOSTIC = 'diagnostic'
    TYPE_PROGRESS = 'progress'
    TYPE_MONTHLY = 'monthly'
    TYPE_CHOICES = [
        (TYPE_DIAGNOSTIC, 'Диагностика'),
        (TYPE_PROGRESS, 'Прогресс'),
        (TYPE_MONTHLY, 'Ежемесячный'),
    ]

    STATUS_GENERATING = 'generating'
    STATUS_READY = 'ready'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_GENERATING, 'Генерируется'),
        (STATUS_READY, 'Готов'),
        (STATUS_FAILED, 'Ошибка'),
    ]

    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='reports')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    result = models.ForeignKey('analytics.AnalyticsResult', on_delete=models.SET_NULL, null=True, blank=True)
    report_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_GENERATING)
    file_url = models.URLField(max_length=500, null=True, blank=True)
    share_token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    share_expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reports'
        indexes = [
            models.Index(fields=['couple', '-created_at']),
            models.Index(fields=['share_token']),
        ]

    def __str__(self):
        return f"Report({self.report_type}, {self.status})"
