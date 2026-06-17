from django.db import models
from shared.models import BaseModel


class RecoveryPlan(BaseModel):
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_PAUSED = 'paused'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_COMPLETED, 'Завершён'),
        (STATUS_PAUSED, 'Пауза'),
    ]

    couple = models.ForeignKey('couples.Couple', on_delete=models.CASCADE, related_name='plans')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    result = models.ForeignKey('analytics.AnalyticsResult', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    duration_weeks = models.SmallIntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recovery_plans'
        indexes = [models.Index(fields=['couple', 'status'])]

    def __str__(self):
        return f"Plan({self.couple_id}, {self.title})"


class PlanTask(BaseModel):
    TASK_TYPE_EXERCISE = 'exercise'
    TASK_TYPE_QUESTION = 'question'
    TASK_TYPE_READING = 'reading'
    TASK_TYPE_PRACTICE = 'practice'
    TASK_TYPE_CHOICES = [
        (TASK_TYPE_EXERCISE, 'Упражнение'),
        (TASK_TYPE_QUESTION, 'Вопрос'),
        (TASK_TYPE_READING, 'Чтение'),
        (TASK_TYPE_PRACTICE, 'Практика'),
    ]

    ASSIGNED_BOTH = 'both'
    ASSIGNED_A = 'partner_a'
    ASSIGNED_B = 'partner_b'
    ASSIGNED_CHOICES = [
        (ASSIGNED_BOTH, 'Оба'),
        (ASSIGNED_A, 'Партнёр A'),
        (ASSIGNED_B, 'Партнёр B'),
    ]

    plan = models.ForeignKey(RecoveryPlan, on_delete=models.CASCADE, related_name='tasks')
    week_number = models.SmallIntegerField()
    day_of_week = models.SmallIntegerField(null=True, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    task_type = models.CharField(max_length=30, choices=TASK_TYPE_CHOICES, default=TASK_TYPE_EXERCISE)
    assigned_to = models.CharField(max_length=20, choices=ASSIGNED_CHOICES, default=ASSIGNED_BOTH)
    order_index = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'plan_tasks'
        indexes = [models.Index(fields=['plan', 'week_number'])]
        ordering = ['week_number', 'day_of_week', 'order_index']

    def __str__(self):
        return f"Task(week={self.week_number}, {self.title[:40]})"


class TaskCompletion(BaseModel):
    task = models.ForeignKey(PlanTask, on_delete=models.CASCADE, related_name='completions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'task_completions'
        unique_together = [['task', 'user']]
        indexes = [models.Index(fields=['task']), models.Index(fields=['user'])]
