from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from shared.models import BaseModel


# Определение 10 уровней диагностики
DIAGNOSTIC_LEVELS = [
    (1,  'Основа отношений',       '🌱', 'Общее состояние и удовлетворённость'),
    (2,  'Коммуникация',           '💬', 'Умение слушать и открытость'),
    (3,  'Доверие',                '🤝', 'Честность, надёжность, безопасность'),
    (4,  'Эмоциональная близость', '❤️', 'Поддержка, понимание, эмоциональная связь'),
    (5,  'Конфликты',              '⚡', 'Причины конфликтов и способы решения'),
    (6,  'Романтика',              '🌹', 'Внимание, нежность, романтическая связь'),
    (7,  'Финансы',                '💰', 'Бюджет, расходы, финансовые цели'),
    (8,  'Родственники',           '👨‍👩‍👧', 'Границы семьи и влияние родных'),
    (9,  'Дети',                   '👶', 'Воспитание и семейная атмосфера'),
    (10, 'Будущее семьи',          '🌟', 'Общие мечты и долгосрочное развитие'),
]

LEVEL_NUMBERS = [row[0] for row in DIAGNOSTIC_LEVELS]


def get_level_meta(level_number: int) -> dict:
    for num, title, emoji, desc in DIAGNOSTIC_LEVELS:
        if num == level_number:
            return {'number': num, 'title': title, 'emoji': emoji, 'description': desc}
    return {'number': 1, 'title': 'Основа отношений', 'emoji': '🌱', 'description': ''}


class Question(BaseModel):
    ZONE_COMMUNICATION = 'communication'
    ZONE_TRUST = 'trust'
    ZONE_INTIMACY = 'intimacy'
    ZONE_CONFLICT = 'conflict'
    ZONE_VALUES = 'values'
    ZONE_FINANCE = 'finance'
    ZONE_RELATIVES = 'relatives'
    ZONE_FUTURE = 'future'
    ZONE_CHOICES = [
        (ZONE_COMMUNICATION, 'Коммуникация'),
        (ZONE_TRUST, 'Доверие'),
        (ZONE_INTIMACY, 'Близость'),
        (ZONE_CONFLICT, 'Конфликты'),
        (ZONE_VALUES, 'Ценности'),
        (ZONE_FINANCE, 'Финансы'),
        (ZONE_RELATIVES, 'Родственники'),
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
    level_number = models.SmallIntegerField(default=1)
    text = models.TextField()
    i18n = models.JSONField(default=dict, blank=True)
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SCALE)
    options = models.JSONField(null=True, blank=True)
    order_index = models.SmallIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'questions'
        ordering = ['level_number', 'zone', 'order_index']
        indexes = [
            models.Index(fields=['level_number', 'is_active']),
            models.Index(fields=['zone', 'is_active']),
        ]

    def __str__(self):
        return f"[L{self.level_number}/{self.zone}] {self.text[:60]}"


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
    level_number = models.SmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'diagnostic_sessions'
        unique_together = [['couple', 'user', 'level_number']]
        indexes = [
            models.Index(fields=['couple', 'user', 'level_number']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Session(L{self.level_number}, {self.user.first_name}, status={self.status})"


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


class FamilyJourney(BaseModel):
    """Путь семейного развития пары — создаётся при активации пары."""
    couple = models.OneToOneField(
        'couples.Couple', on_delete=models.CASCADE, related_name='journey'
    )
    max_unlocked_level = models.SmallIntegerField(default=1)
    last_completed_level = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'family_journeys'

    def __str__(self):
        return f"Journey({self.couple}, unlocked={self.max_unlocked_level})"


class LevelProgress(BaseModel):
    """Прогресс пары по конкретному уровню диагностики."""
    journey = models.ForeignKey(FamilyJourney, on_delete=models.CASCADE, related_name='level_progress')
    level_number = models.SmallIntegerField()

    partner_a_done = models.BooleanField(default=False)
    partner_b_done = models.BooleanField(default=False)
    both_diagnosed_at = models.DateTimeField(null=True, blank=True)
    practices_done_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'level_progress'
        unique_together = [['journey', 'level_number']]
        ordering = ['level_number']

    def __str__(self):
        return f"LevelProgress(L{self.level_number}, done={self.completed_at is not None})"

    @property
    def status(self) -> str:
        if self.completed_at:
            return 'completed'
        if self.both_diagnosed_at:
            return 'diagnosed'
        if self.partner_a_done or self.partner_b_done:
            return 'in_progress'
        return 'unlocked'
