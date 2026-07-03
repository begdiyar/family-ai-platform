import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from shared.models import BaseModel


GENDER_CHOICES = [
    ('male',              'Мужчина'),
    ('female',            'Женщина'),
    ('other',             'Другое'),
    ('prefer_not_to_say', 'Предпочитаю не указывать'),
]

EDUCATION_CHOICES = [
    ('secondary',          'Среднее'),
    ('vocational',         'Среднее специальное'),
    ('incomplete_higher',  'Неполное высшее'),
    ('higher',             'Высшее'),
    ('postgraduate',       'Учёная степень'),
]

CONFLICT_STYLE_CHOICES = [
    ('avoidant',        'Избегающий'),
    ('confrontational', 'Конфронтационный'),
    ('collaborative',   'Совместное решение'),
    ('competitive',     'Соревновательный'),
    ('compromising',    'Компромисс'),
]

SUPPORT_STYLE_CHOICES = [
    ('advice',    'Советы и решения'),
    ('empathy',   'Сочувствие и понимание'),
    ('practical', 'Практическая помощь'),
    ('space',     'Пространство для осмысления'),
]


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Номер телефона обязателен')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, default='')
    native_language = models.CharField(max_length=10, blank=True, default='')
    occupation = models.CharField(max_length=100, blank=True, default='')
    education_level = models.CharField(max_length=30, choices=EDUCATION_CHOICES, blank=True, default='')
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default='ru')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return self.phone

    def get_active_couple(self):
        from apps.couples.repositories import CoupleRepository
        return CoupleRepository.get_active_for_user(self)


class CommunicationPreference(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='communication_pref',
    )
    conflict_style = models.CharField(
        max_length=30, choices=CONFLICT_STYLE_CHOICES, blank=True, default='',
    )
    support_style = models.CharField(
        max_length=30, choices=SUPPORT_STYLE_CHOICES, blank=True, default='',
    )

    class Meta:
        db_table = 'communication_preferences'

    def __str__(self):
        return f'CommPref({self.user.email})'
