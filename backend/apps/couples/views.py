from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shared.exceptions import NotFoundError
from .repositories import CoupleRepository
from .serializers import CoupleDetailSerializer, InviteSerializer, AcceptInviteSerializer
from .services import CoupleService, InviteService


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
