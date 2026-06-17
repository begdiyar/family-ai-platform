from django.conf import settings
from django.db import transaction

from shared.exceptions import BusinessLogicError, NotFoundError
from shared.utils import generate_token, future_datetime
from apps.users.models import User
from .models import Couple, CoupleInvite
from .repositories import CoupleRepository, InviteRepository


class InviteService:
    INVITE_TTL_HOURS = 72

    @classmethod
    def create_for_couple(cls, couple: Couple, invited_by: User) -> CoupleInvite:
        InviteRepository.expire_pending_for_couple(couple)
        token = generate_token(48)
        expires_at = future_datetime(hours=cls.INVITE_TTL_HOURS)
        return InviteRepository.create(
            couple=couple,
            invited_by=invited_by,
            token=token,
            expires_at=expires_at,
        )

    @staticmethod
    def build_invite_url(token: str) -> str:
        return f"{settings.FRONTEND_URL}/invite/{token}"


class CoupleService:
    @staticmethod
    def create_couple(user: User) -> dict:
        if CoupleRepository.has_active_couple(user):
            raise BusinessLogicError('ALREADY_IN_COUPLE', 'Вы уже состоите в паре')
        couple = CoupleRepository.create(partner_a=user)
        invite = InviteService.create_for_couple(couple, invited_by=user)
        return {'couple': couple, 'invite': invite}

    @staticmethod
    def accept_invite(token: str, user: User) -> Couple:
        with transaction.atomic():
            # of=('self',) — блокируем только строку инвайта, без JOIN на nullable partner_b
            invite = (
                CoupleInvite.objects
                .select_for_update(of=('self',))
                .select_related('couple__partner_a', 'couple__partner_b')
                .filter(token=token, status=CoupleInvite.STATUS_PENDING)
                .first()
            )
            if not invite or invite.is_expired():
                raise NotFoundError('INVITE_NOT_FOUND', 'Приглашение не найдено или истекло')
            if str(invite.couple.partner_a_id) == str(user.id):
                raise BusinessLogicError('CANNOT_ACCEPT_OWN_INVITE', 'Нельзя принять собственное приглашение')
            if CoupleRepository.has_active_couple(user):
                raise BusinessLogicError('ALREADY_IN_COUPLE', 'Вы уже состоите в паре')
            couple = CoupleRepository.activate(invite.couple, partner_b=user)
            InviteRepository.accept(invite)
        return couple

    @staticmethod
    def regenerate_invite(user: User) -> CoupleInvite:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            # Ищем pending пару где user = partner_a
            from .models import Couple as C
            couple = C.objects.filter(partner_a=user, status=C.STATUS_PENDING).first()
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Сначала создайте пару')
        return InviteService.create_for_couple(couple, invited_by=user)
