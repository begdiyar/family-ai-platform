from django.db import models as django_models
from django.utils import timezone
from typing import Optional

from .models import Couple, CoupleInvite
from apps.users.models import User


class CoupleRepository:
    @staticmethod
    def get_active_for_user(user: User) -> Optional[Couple]:
        return (
            Couple.objects
            .filter(
                django_models.Q(partner_a=user) | django_models.Q(partner_b=user),
                status__in=[Couple.STATUS_ACTIVE, Couple.STATUS_PENDING],
            )
            .select_related('partner_a', 'partner_b')
            .order_by('-created_at')
            .first()
        )

    @staticmethod
    def has_active_couple(user: User) -> bool:
        return Couple.objects.filter(
            django_models.Q(partner_a=user) | django_models.Q(partner_b=user),
            status__in=[Couple.STATUS_ACTIVE, Couple.STATUS_PENDING],
        ).exists()

    @staticmethod
    def create(partner_a: User) -> Couple:
        return Couple.objects.create(partner_a=partner_a, status=Couple.STATUS_PENDING)

    @staticmethod
    def activate(couple: Couple, partner_b: User) -> Couple:
        couple.partner_b = partner_b
        couple.status = Couple.STATUS_ACTIVE
        couple.save(update_fields=['partner_b', 'status', 'updated_at'])
        return couple

    @staticmethod
    def get_by_id(couple_id) -> Optional[Couple]:
        return (
            Couple.objects
            .filter(id=couple_id)
            .select_related('partner_a', 'partner_b')
            .first()
        )


class InviteRepository:
    @staticmethod
    def create(couple: Couple, invited_by: User, token: str, expires_at) -> CoupleInvite:
        return CoupleInvite.objects.create(
            couple=couple,
            invited_by=invited_by,
            token=token,
            expires_at=expires_at,
        )

    @staticmethod
    def get_valid(token: str) -> Optional[CoupleInvite]:
        return (
            CoupleInvite.objects
            .filter(
                token=token,
                status=CoupleInvite.STATUS_PENDING,
                expires_at__gt=timezone.now(),
            )
            .select_related('couple__partner_a', 'couple__partner_b')
            .first()
        )

    @staticmethod
    def accept(invite: CoupleInvite) -> None:
        invite.status = CoupleInvite.STATUS_ACCEPTED
        invite.accepted_at = timezone.now()
        invite.save(update_fields=['status', 'accepted_at', 'updated_at'])

    @staticmethod
    def expire_pending_for_couple(couple: Couple) -> None:
        CoupleInvite.objects.filter(
            couple=couple,
            status=CoupleInvite.STATUS_PENDING,
        ).update(status=CoupleInvite.STATUS_EXPIRED)

    @staticmethod
    def get_active_for_couple(couple: Couple) -> Optional[CoupleInvite]:
        return CoupleInvite.objects.filter(
            couple=couple,
            status=CoupleInvite.STATUS_PENDING,
            expires_at__gt=timezone.now(),
        ).first()
