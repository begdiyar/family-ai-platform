from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ConflictSession
from .serializers import ConflictSessionSerializer, ConflictSessionDetailSerializer, SubmitEntrySerializer
from .services import MediationService


class ConflictSessionListView(APIView):
    def get(self, request):
        from apps.couples.repositories import CoupleRepository
        couple = CoupleRepository.require_full_couple(request.user)
        sessions = ConflictSession.objects.filter(couple=couple).order_by('-created_at')[:20]
        return Response(ConflictSessionSerializer(sessions, many=True, context={'user': request.user}).data)

    def post(self, request):
        title = request.data.get('title', 'Конфликт')
        session = MediationService.create_session(request.user, title)
        return Response(ConflictSessionSerializer(session, context={'user': request.user}).data,
                        status=status.HTTP_201_CREATED)


class ConflictSessionDetailView(APIView):
    def get(self, request, session_id):
        session = get_object_or_404(ConflictSession, id=session_id)
        return Response(ConflictSessionDetailSerializer(session, context={'user': request.user}).data)


class SubmitEntryView(APIView):
    def post(self, request, session_id):
        session = get_object_or_404(ConflictSession, id=session_id)
        serializer = SubmitEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        entry = MediationService.submit_entry(
            session, request.user,
            description=d['description'],
            feelings=d.get('feelings', ''),
            desired_outcome=d.get('desired_outcome', ''),
        )
        return Response({'success': True, 'both_submitted': session.both_submitted()})
