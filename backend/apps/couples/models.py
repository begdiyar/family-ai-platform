from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from shared.models import BaseModel


RELATIONSHIP_STATUS_CHOICES = [
    ('dating',       'Встречаемся'),
    ('engaged',      'Помолвлены'),
    ('cohabitating', 'Живём вместе'),
    ('married',      'Женаты/замужем'),
    ('separated',    'Живём раздельно'),
]

CHILD_GENDER_CHOICES = [
    ('male',   'Мальчик'),
    ('female', 'Девочка'),
]

_LEVEL_VALIDATORS = [MinValueValidator(1), MaxValueValidator(5)]


class FamilyValue(models.Model):
    slug     = models.CharField(max_length=30, unique=True)
    label_ru = models.CharField(max_length=100)

    class Meta:
        db_table = 'family_values'
        ordering = ['label_ru']

    def __str__(self):
        return f'{self.slug}: {self.label_ru}'


class Couple(BaseModel):
    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_PAUSED = 'paused'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидание'),
        (STATUS_ACTIVE, 'Активна'),
        (STATUS_PAUSED, 'Пауза'),
    ]

    partner_a = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='couples_as_a',
    )
    partner_b = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='couples_as_b',
        null=True, blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Relationship identity
    relationship_status    = models.CharField(
        max_length=20, choices=RELATIONSHIP_STATUS_CHOICES, blank=True, default='',
    )
    relationship_start_date = models.DateField(null=True, blank=True)
    marriage_date           = models.DateField(null=True, blank=True)

    # Children (legacy counters kept for backwards compat)
    has_children    = models.BooleanField(default=False)
    children_count  = models.SmallIntegerField(default=0)
    marriage_year   = models.SmallIntegerField(null=True, blank=True)

    # Family context
    lives_with_parents               = models.BooleanField(default=False)
    relatives_influence_level        = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=_LEVEL_VALIDATORS,
    )
    religious_traditions_importance  = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=_LEVEL_VALIDATORS,
    )

    # Family values (M2M)
    family_values = models.ManyToManyField(
        FamilyValue, blank=True, related_name='couples',
    )

    class Meta:
        db_table = 'couples'
        indexes = [
            models.Index(fields=['partner_a']),
            models.Index(fields=['partner_b']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Couple({self.partner_a.first_name} & {self.partner_b.first_name if self.partner_b else '?'})"

    def get_partner(self, user):
        if str(self.partner_a_id) == str(user.id):
            return self.partner_b
        return self.partner_a


class Child(BaseModel):
    couple     = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='children')
    birth_date = models.DateField()
    gender     = models.CharField(
        max_length=10, choices=CHILD_GENDER_CHOICES, blank=True, default='',
    )

    class Meta:
        db_table = 'children'
        ordering = ['birth_date']

    def __str__(self):
        return f'Child(couple={self.couple_id}, {self.birth_date})'


class CoupleInvite(BaseModel):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_EXPIRED = 'expired'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидание'),
        (STATUS_ACCEPTED, 'Принято'),
        (STATUS_EXPIRED, 'Истекло'),
    ]

    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='invites')
    invited_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    class Meta:
        db_table = 'couple_invites'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['couple']),
        ]

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()

    def __str__(self):
        return f"Invite({self.token[:8]}... status={self.status})"
