from rest_framework.permissions import BasePermission
from shared.exceptions import ForbiddenError


class IsCouplePartner(BasePermission):
    """Доступ разрешён, если объект принадлежит паре текущего пользователя."""

    def has_object_permission(self, request, view, obj):
        couple = getattr(request.user, '_cached_couple', None)
        if couple is None:
            from apps.couples.repositories import CoupleRepository
            couple = CoupleRepository.get_active_for_user(request.user)
            request.user._cached_couple = couple
        if couple is None:
            return False
        return str(getattr(obj, 'couple_id', None)) == str(couple.id)


class IsOwner(BasePermission):
    """Доступ разрешён только владельцу объекта (obj.user == request.user)."""

    def has_object_permission(self, request, view, obj):
        return str(getattr(obj, 'user_id', None)) == str(request.user.id)
