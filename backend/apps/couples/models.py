from django.db import models
from django.utils import timezone
from shared.models import BaseModel


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
        'users.User', on_delete=models.CASCADE, related_name='couples_as_a'
    )
    partner_b = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='couples_as_b',
        null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    has_children = models.BooleanField(default=False)
    children_count = models.SmallIntegerField(default=0)
    marriage_year = models.SmallIntegerField(null=True, blank=True)

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
