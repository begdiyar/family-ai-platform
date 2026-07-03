import uuid
from django.db import models
from shared.models import BaseModel

# Slot types that can be marked completed by the user
COMPLETABLE_SLOTS = ['main', 'conversation', 'gesture', 'activity', 'ritual']

# Display order for serialization
SLOT_ORDER = ['main', 'conversation', 'gesture', 'activity', 'ritual', 'growth']

# 10-level XP system  (min_xp, max_xp, level, label, emoji)
FAMILY_LEVELS = [
    (0,   9,   1,  'Первые шаги',          '🌱'),
    (10,  24,  2,  'Начало пути',           '🌿'),
    (25,  49,  3,  'Набираем темп',         '🌀'),
    (50,  84,  4,  'Устойчивый рост',       '⚡'),
    (85,  129, 5,  'Укрепляем фундамент',   '🔥'),
    (130, 184, 6,  'Зрелая пара',           '⭐'),
    (185, 249, 7,  'Мастера близости',      '💎'),
    (250, 324, 8,  'Гармоничный союз',      '🏅'),
    (325, 409, 9,  'Пример для других',     '🌟'),
    (410, 9999, 10, 'Образцовая семья',     '🏆'),
]

# Stage (1-5) per level  →  (stage_num, stage_name, stage_emoji)
STAGE_BY_LEVEL = {
    1:  (1, 'Восстановление связи',   '🌱'),
    2:  (1, 'Восстановление связи',   '🌱'),
    3:  (2, 'Улучшение общения',      '🌿'),
    4:  (2, 'Улучшение общения',      '🌿'),
    5:  (3, 'Укрепление доверия',     '🌀'),
    6:  (3, 'Укрепление доверия',     '🌀'),
    7:  (4, 'Эмоциональная близость', '💎'),
    8:  (4, 'Эмоциональная близость', '💎'),
    9:  (5, 'Долгосрочное развитие',  '🌟'),
    10: (5, 'Долгосрочное развитие',  '🌟'),
}


class PracticeCategory(models.TextChoices):
    COMMUNICATION = 'communication', 'Коммуникация'
    TRUST         = 'trust',         'Доверие'
    INTIMACY      = 'intimacy',      'Близость'
    GRATITUDE     = 'gratitude',     'Благодарность'
    CHILDREN      = 'children',      'Дети'
    FINANCES      = 'finances',      'Финансы'
    RELATIVES     = 'relatives',     'Родственники'
    ROMANCE       = 'romance',       'Романтика'


class SlotType(models.TextChoices):
    MAIN         = 'main',         'Практика дня'
    CONVERSATION = 'conversation', 'Тема разговора'
    GESTURE      = 'gesture',      'Маленький жест любви'
    ACTIVITY     = 'activity',     'Семейная активность'
    RITUAL       = 'ritual',       'Ритуал пары'
    GROWTH       = 'growth',       'Рекомендация для роста'


class PracticeDifficulty(models.TextChoices):
    EASY   = 'easy',   'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD   = 'hard',   'Сложный'


class Practice(BaseModel):
    title            = models.CharField(max_length=200)
    description      = models.TextField()
    instructions     = models.TextField(blank=True)
    category         = models.CharField(max_length=30, choices=PracticeCategory.choices, db_index=True)
    slot_type        = models.CharField(max_length=20, choices=SlotType.choices, db_index=True)
    difficulty       = models.CharField(max_length=20, choices=PracticeDifficulty.choices, default=PracticeDifficulty.EASY)
    duration_minutes = models.PositiveSmallIntegerField(default=10)
    is_active        = models.BooleanField(default=True, db_index=True)
    # {"en": {"title": "...", "description": "...", "instructions": "..."}, "uz": {...}}
    i18n             = models.JSONField(default=dict, blank=True)
    # Free-form tags for additional filtering, e.g. ["anger", "listening", "physical_touch"]
    tags             = models.JSONField(default=list, blank=True)
    # For growth slot: linked Academy article to navigate to
    academy_article  = models.ForeignKey(
        'academy.Article', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='linked_practices',
    )

    class Meta:
        db_table = 'practices'
        ordering = ['category', 'slot_type', 'difficulty', 'title']

    def __str__(self):
        return f'[{self.get_category_display()}/{self.get_slot_type_display()}] {self.title}'


class DailyAssignment(BaseModel):
    couple           = models.ForeignKey(
        'couples.Couple', on_delete=models.CASCADE, related_name='daily_assignments',
    )
    date             = models.DateField()
    categories_used  = models.JSONField(default=list, blank=True)
    is_ai_generated  = models.BooleanField(default=False)

    class Meta:
        db_table        = 'daily_assignments'
        unique_together = [['couple', 'date']]
        indexes         = [models.Index(fields=['couple', '-date'])]

    def __str__(self):
        return f'Assignment({self.couple_id}, {self.date})'

    @property
    def completed_count(self):
        return sum(
            1 for s in self.slots.all()
            if s.completed and s.slot_type in COMPLETABLE_SLOTS
        )

    @property
    def total_completable(self):
        return len(COMPLETABLE_SLOTS)

    @property
    def is_fully_completed(self):
        return self.completed_count == self.total_completable


class AssignmentSlot(BaseModel):
    assignment   = models.ForeignKey(
        DailyAssignment, on_delete=models.CASCADE, related_name='slots',
    )
    slot_type    = models.CharField(max_length=20, choices=SlotType.choices, db_index=True)
    practice     = models.ForeignKey(
        Practice, null=True, blank=True, on_delete=models.SET_NULL, related_name='slots',
    )
    completed    = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table        = 'assignment_slots'
        unique_together = [['assignment', 'slot_type']]

    def __str__(self):
        mark = '✓' if self.completed else '○'
        return f'Slot({self.assignment_id}, {self.slot_type}, {mark})'


class FamilyDevelopmentPlan(BaseModel):
    """
    One-per-couple plan that tracks level, stage, and priority zones
    derived from the couple's latest diagnostic results.
    """
    couple          = models.OneToOneField(
        'couples.Couple', on_delete=models.CASCADE, related_name='development_plan',
    )
    priority_zone   = models.CharField(max_length=30, blank=True, default='')
    secondary_zone  = models.CharField(max_length=30, blank=True, default='')
    tertiary_zone   = models.CharField(max_length=30, blank=True, default='')
    current_level   = models.PositiveSmallIntegerField(default=1)
    current_stage   = models.PositiveSmallIntegerField(default=1)
    # Cached counter of completed completable slots — updated on each completion
    total_completed = models.PositiveIntegerField(default=0)
    last_diagnostic_at = models.DateTimeField(null=True, blank=True)
    next_diagnostic_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'family_development_plans'

    def __str__(self):
        return f'Plan(couple={self.couple_id}, L{self.current_level}, {self.total_completed} xp)'

    def recalculate_level(self) -> None:
        for min_v, max_v, level, _label, _emoji in FAMILY_LEVELS:
            if min_v <= self.total_completed <= max_v:
                self.current_level = level
                break
        else:
            self.current_level = 10
        self.current_stage = STAGE_BY_LEVEL.get(self.current_level, (1, '', ''))[0]
