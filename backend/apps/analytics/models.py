from django.db import models
from shared.models import BaseModel


class AnalyticsResult(BaseModel):
    CRISIS_NONE = 'none'
    CRISIS_WARNING = 'warning'
    CRISIS_CRITICAL = 'critical'
    CRISIS_CHOICES = [
        (CRISIS_NONE, 'Нет'),
        (CRISIS_WARNING, 'Предупреждение'),
        (CRISIS_CRITICAL, 'Кризис'),
    ]

    RELATIVES_LOW = 'low'
    RELATIVES_MEDIUM = 'medium'
    RELATIVES_HIGH = 'high'
    RELATIVES_CHOICES = [
        (RELATIVES_LOW, 'Низкое'),
        (RELATIVES_MEDIUM, 'Среднее'),
        (RELATIVES_HIGH, 'Высокое'),
    ]

    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='analytics_results')
    session_a = models.ForeignKey('diagnostics.DiagnosticSession', on_delete=models.CASCADE, related_name='result_as_a')
    session_b = models.ForeignKey('diagnostics.DiagnosticSession', on_delete=models.CASCADE, related_name='result_as_b')
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    key_insights = models.JSONField(null=True, blank=True)

    # Новые поля
    crisis_level = models.CharField(max_length=20, choices=CRISIS_CHOICES, default=CRISIS_NONE)
    bridge_analysis = models.JSONField(null=True, blank=True)
    strengths_summary = models.JSONField(null=True, blank=True)
    problem_chain = models.JSONField(null=True, blank=True)
    relatives_index = models.CharField(max_length=20, choices=RELATIVES_CHOICES, null=True, blank=True)
    finance_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    child_environment_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'analytics_results'
        indexes = [
            models.Index(fields=['couple', '-created_at']),
        ]

    def __str__(self):
        return f"Result(couple={self.couple_id}, score={self.overall_score})"

    @property
    def is_crisis(self):
        return self.crisis_level in (self.CRISIS_WARNING, self.CRISIS_CRITICAL)


class ZoneScore(BaseModel):
    ZONE_CHOICES = [
        ('communication', 'Коммуникация'),
        ('trust', 'Доверие'),
        ('intimacy', 'Близость'),
        ('conflict', 'Конфликты'),
        ('values', 'Ценности'),
        ('future', 'Будущее'),
    ]

    result = models.ForeignKey(AnalyticsResult, on_delete=models.CASCADE, related_name='zone_scores')
    zone = models.CharField(max_length=30, choices=ZONE_CHOICES)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'zone_scores'
        unique_together = [['result', 'zone', 'user']]
        indexes = [models.Index(fields=['result', 'zone'])]

    @property
    def percent(self):
        if self.max_score:
            return round(float(self.score) / float(self.max_score) * 100)
        return 0
