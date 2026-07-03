from django.db import models
from django.conf import settings
from shared.models import BaseModel


class ArticleSource(BaseModel):
    SOURCE_RESEARCHER = 'researcher'
    SOURCE_ORGANIZATION = 'organization'
    SOURCE_BOOK = 'book'
    SOURCE_JOURNAL = 'journal'
    SOURCE_CHOICES = [
        (SOURCE_RESEARCHER, 'Исследователь'),
        (SOURCE_ORGANIZATION, 'Организация'),
        (SOURCE_BOOK, 'Книга'),
        (SOURCE_JOURNAL, 'Журнал'),
    ]

    TRUST_HIGH = 'high'
    TRUST_MEDIUM = 'medium'
    TRUST_CHOICES = [
        (TRUST_HIGH, 'Высокий'),
        (TRUST_MEDIUM, 'Средний'),
    ]

    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    trust_level = models.CharField(max_length=10, choices=TRUST_CHOICES, default=TRUST_HIGH)
    url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'academy_sources'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(BaseModel):
    CATEGORY_COMMUNICATION = 'communication'
    CATEGORY_TRUST = 'trust'
    CATEGORY_CONFLICT = 'conflict'
    CATEGORY_INTIMACY = 'intimacy'
    CATEGORY_LOVE = 'love'
    CATEGORY_FINANCE = 'finance'
    CATEGORY_HUSBAND_ROLE = 'husband_role'
    CATEGORY_WIFE_ROLE = 'wife_role'
    CATEGORY_RELATIVES = 'relatives'
    CATEGORY_PARENTING = 'parenting'
    CATEGORY_TRADITIONS = 'traditions'
    CATEGORY_STRESS = 'stress'
    CATEGORY_MARRIAGE_PREP = 'marriage_prep'
    CATEGORY_CRISIS = 'crisis_recovery'
    CATEGORY_CHOICES = [
        (CATEGORY_COMMUNICATION, 'Общение в семье'),
        (CATEGORY_TRUST, 'Доверие'),
        (CATEGORY_CONFLICT, 'Управление конфликтами'),
        (CATEGORY_INTIMACY, 'Эмоциональная близость'),
        (CATEGORY_LOVE, 'Любовь и уважение'),
        (CATEGORY_FINANCE, 'Финансы в семье'),
        (CATEGORY_HUSBAND_ROLE, 'Роль мужа'),
        (CATEGORY_WIFE_ROLE, 'Роль жены'),
        (CATEGORY_RELATIVES, 'Отношения с родственниками'),
        (CATEGORY_PARENTING, 'Воспитание детей'),
        (CATEGORY_TRADITIONS, 'Семейные традиции'),
        (CATEGORY_STRESS, 'Стресс и выгорание'),
        (CATEGORY_MARRIAGE_PREP, 'Подготовка к браку'),
        (CATEGORY_CRISIS, 'Восстановление после кризиса'),
    ]

    DIFFICULTY_BEGINNER = 'beginner'
    DIFFICULTY_INTERMEDIATE = 'intermediate'
    DIFFICULTY_ADVANCED = 'advanced'
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_BEGINNER, 'Начальный'),
        (DIFFICULTY_INTERMEDIATE, 'Средний'),
        (DIFFICULTY_ADVANCED, 'Продвинутый'),
    ]

    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=300)
    brief = models.TextField()
    body = models.TextField()
    read_time_minutes = models.PositiveSmallIntegerField(default=5)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default=DIFFICULTY_BEGINNER)
    tags = models.JSONField(default=list)
    sources = models.ManyToManyField(ArticleSource, blank=True, related_name='articles')
    is_published = models.BooleanField(default=True)
    order_index = models.SmallIntegerField(default=0)
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'academy_articles'
        ordering = ['category', 'order_index']
        indexes = [
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f'[{self.category}] {self.title}'


class Training(BaseModel):
    SKILL_LISTENING = 'active_listening'
    SKILL_EMOTIONS = 'emotion_management'
    SKILL_GRATITUDE = 'gratitude'
    SKILL_SUPPORT = 'partner_support'
    SKILL_DIALOGUE = 'constructive_dialogue'
    SKILL_CONFLICT = 'conflict_resolution'
    SKILL_PLANNING = 'joint_planning'
    SKILL_CHOICES = [
        (SKILL_LISTENING, 'Активное слушание'),
        (SKILL_EMOTIONS, 'Управление эмоциями'),
        (SKILL_GRATITUDE, 'Навык благодарности'),
        (SKILL_SUPPORT, 'Поддержка партнёра'),
        (SKILL_DIALOGUE, 'Конструктивный диалог'),
        (SKILL_CONFLICT, 'Решение конфликтов'),
        (SKILL_PLANNING, 'Совместное планирование'),
    ]

    DIFFICULTY_CHOICES = Article.DIFFICULTY_CHOICES

    slug = models.SlugField(max_length=200, unique=True)
    skill_type = models.CharField(max_length=30, choices=SKILL_CHOICES)
    title = models.CharField(max_length=300)
    description = models.TextField()
    theory = models.TextField()
    exercise_instruction = models.TextField()
    completion_check = models.TextField()
    duration_minutes = models.PositiveSmallIntegerField(default=10)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    order_index = models.SmallIntegerField(default=0)
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'academy_trainings'
        ordering = ['order_index']

    def __str__(self):
        return self.title


class Program(BaseModel):
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    duration_days = models.PositiveSmallIntegerField()
    category_focus = models.CharField(max_length=50)
    cover_gradient = models.CharField(max_length=200, default='linear-gradient(135deg, #6558A8, #4A88B8)')
    order_index = models.SmallIntegerField(default=0)
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'academy_programs'
        ordering = ['order_index']

    def __str__(self):
        return f'{self.title} ({self.duration_days} дней)'


class ProgramDay(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=300)
    material = models.TextField()
    exercise = models.TextField()
    reflection_prompt = models.TextField()
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'academy_program_days'
        ordering = ['day_number']
        unique_together = [['program', 'day_number']]

    def __str__(self):
        return f'{self.program.title} — День {self.day_number}'


class AcademyMicroPractice(BaseModel):
    title = models.CharField(max_length=300)
    instruction = models.TextField()
    category = models.CharField(max_length=30, choices=Article.CATEGORY_CHOICES)
    duration_minutes = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order_index = models.SmallIntegerField(default=0)
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'academy_micro_practices'
        ordering = ['order_index']

    def __str__(self):
        return self.title


class UserArticleProgress(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_progress'
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='user_progress')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academy_user_article_progress'
        unique_together = [['user', 'article']]
        indexes = [models.Index(fields=['user'])]


class UserTrainingProgress(BaseModel):
    STATUS_STARTED = 'started'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_STARTED, 'Начата'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='training_progress'
    )
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_STARTED)
    reflection_note = models.TextField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'academy_user_training_progress'
        unique_together = [['user', 'training']]
        indexes = [models.Index(fields=['user'])]


class UserProgramEnrollment(BaseModel):
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_PAUSED = 'paused'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активна'),
        (STATUS_COMPLETED, 'Завершена'),
        (STATUS_PAUSED, 'Пауза'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='program_enrollments'
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='enrollments')
    current_day = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academy_user_program_enrollments'
        unique_together = [['user', 'program']]
        indexes = [models.Index(fields=['user', 'status'])]


class UserProgramDayProgress(BaseModel):
    enrollment = models.ForeignKey(
        UserProgramEnrollment, on_delete=models.CASCADE, related_name='day_progress'
    )
    day = models.ForeignKey(ProgramDay, on_delete=models.CASCADE)
    reflection = models.TextField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academy_user_program_day_progress'
        unique_together = [['enrollment', 'day']]
        indexes = [models.Index(fields=['enrollment'])]


class UserMicroPracticeLog(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='micro_practice_logs'
    )
    practice = models.ForeignKey(AcademyMicroPractice, on_delete=models.CASCADE)
    date = models.DateField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academy_user_micro_practice_logs'
        unique_together = [['user', 'date']]
        indexes = [models.Index(fields=['user', 'date'])]


class Achievement(BaseModel):
    CONDITION_ARTICLES = 'articles_count'
    CONDITION_TRAININGS = 'trainings_count'
    CONDITION_PROGRAMS = 'programs_count'
    CONDITION_STREAK = 'streak_days'
    CONDITION_CHOICES = [
        (CONDITION_ARTICLES, 'Количество статей'),
        (CONDITION_TRAININGS, 'Количество тренировок'),
        (CONDITION_PROGRAMS, 'Количество программ'),
        (CONDITION_STREAK, 'Серия дней'),
    ]

    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10)
    condition_type = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    condition_value = models.IntegerField()
    i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'academy_achievements'
        ordering = ['condition_type', 'condition_value']

    def __str__(self):
        return f'{self.icon} {self.title}'


class UserAchievement(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements'
    )
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'academy_user_achievements'
        unique_together = [['user', 'achievement']]
        indexes = [models.Index(fields=['user'])]
