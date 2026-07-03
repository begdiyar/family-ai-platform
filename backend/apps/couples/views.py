from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shared.exceptions import NotFoundError
from .models import Child, FamilyValue
from .repositories import CoupleRepository
from .serializers import (
    CoupleDetailSerializer, InviteSerializer, AcceptInviteSerializer,
    ChildSerializer, ChildCreateSerializer,
    FamilyContextSerializer, FamilyValueSerializer, FamilyValuesUpdateSerializer,
)
from .services import CoupleService, InviteService


# ── Couple core ───────────────────────────────────────────────────────────────

class CoupleCreateView(APIView):
    def post(self, request):
        result = CoupleService.create_couple(request.user)
        couple = result['couple']
        invite = result['invite']
        data = CoupleDetailSerializer(couple, context={'request': request}).data
        data['invite'] = InviteSerializer(invite).data
        return Response(data, status=status.HTTP_201_CREATED)


class CoupleDetailView(APIView):
    def get(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Вы не состоите в активной паре')
        return Response(CoupleDetailSerializer(couple, context={'request': request}).data)


class InviteAcceptView(APIView):
    def post(self, request):
        serializer = AcceptInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        couple = CoupleService.accept_invite(
            token=serializer.validated_data['token'],
            user=request.user,
        )
        return Response(CoupleDetailSerializer(couple, context={'request': request}).data)


class InviteRegenerateView(APIView):
    def post(self, request):
        invite = CoupleService.regenerate_invite(request.user)
        return Response(InviteSerializer(invite).data)


# ── Children ──────────────────────────────────────────────────────────────────

class ChildrenView(APIView):
    def _get_couple(self, user):
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Вы не состоите в активной паре')
        return couple

    def get(self, request):
        couple = self._get_couple(request.user)
        children = Child.objects.filter(couple=couple).order_by('birth_date')
        return Response(ChildSerializer(children, many=True).data)

    def post(self, request):
        couple = self._get_couple(request.user)
        serializer = ChildCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        child = Child.objects.create(couple=couple, **serializer.validated_data)
        # Keep legacy counters in sync
        cnt = Child.objects.filter(couple=couple).count()
        couple.children_count = cnt
        couple.has_children = cnt > 0
        couple.save(update_fields=['children_count', 'has_children', 'updated_at'])
        return Response(ChildSerializer(child).data, status=status.HTTP_201_CREATED)


class ChildDetailView(APIView):
    def _get_child(self, user, child_id):
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Вы не состоите в активной паре')
        try:
            return Child.objects.get(id=child_id, couple=couple), couple
        except Child.DoesNotExist:
            raise NotFoundError('NOT_FOUND', 'Ребёнок не найден')

    def delete(self, request, child_id):
        child, couple = self._get_child(request.user, child_id)
        child.delete()
        cnt = Child.objects.filter(couple=couple).count()
        couple.children_count = cnt
        couple.has_children = cnt > 0
        couple.save(update_fields=['children_count', 'has_children', 'updated_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Family context ────────────────────────────────────────────────────────────

class FamilyContextView(APIView):
    def _get_couple(self, user):
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Вы не состоите в активной паре')
        return couple

    def get(self, request):
        couple = self._get_couple(request.user)
        return Response(FamilyContextSerializer(couple).data)

    def patch(self, request):
        couple = self._get_couple(request.user)
        serializer = FamilyContextSerializer(couple, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(FamilyContextSerializer(couple).data)


# ── Family values ─────────────────────────────────────────────────────────────

class FamilyValuesListView(APIView):
    """List all available FamilyValue choices."""
    def get(self, request):
        values = FamilyValue.objects.all()
        return Response(FamilyValueSerializer(values, many=True).data)


class CoupleFamilyValuesView(APIView):
    """Get or replace the couple's selected family values."""

    def _get_couple(self, user):
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Вы не состоите в активной паре')
        return couple

    def get(self, request):
        couple = self._get_couple(request.user)
        return Response(FamilyValueSerializer(couple.family_values.all(), many=True).data)

    def put(self, request):
        couple = self._get_couple(request.user)
        serializer = FamilyValuesUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = FamilyValue.objects.filter(slug__in=serializer.validated_data['slugs'])
        couple.family_values.set(values)
        return Response(FamilyValueSerializer(couple.family_values.all(), many=True).data)
