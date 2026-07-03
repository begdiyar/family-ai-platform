from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import DiagnosticSession
from .repositories import QuestionRepository
from .serializers import (
    QuestionSerializer, SessionSerializer,
    SaveAnswersSerializer, StartSessionSerializer,
)
from .services import DiagnosticService, JourneyService


class QuestionsView(APIView):
    def get(self, request):
        level_number = int(request.query_params.get('level', 1))
        questions = QuestionRepository.get_by_level(level_number)
        return Response({
            'level_number': level_number,
            'total': len(questions),
            'questions': QuestionSerializer(questions, many=True, context={'request': request}).data,
        })


class SessionCreateView(APIView):
    def post(self, request):
        serializer = StartSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        level_number = serializer.validated_data['level_number']
        session = DiagnosticService.start_session(request.user, level_number)
        return Response(SessionSerializer(session).data, status=status.HTTP_201_CREATED)


class CurrentSessionView(APIView):
    def get(self, request):
        session = DiagnosticService.get_current_session(request.user)
        return Response(SessionSerializer(session).data)


class SaveAnswersView(APIView):
    def post(self, request, session_id):
        session = get_object_or_404(DiagnosticSession, id=session_id)
        serializer = SaveAnswersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = DiagnosticService.save_answers(
            session=session,
            user=request.user,
            answers_data=serializer.validated_data['answers'],
        )
        return Response(result)


class CompleteSessionView(APIView):
    def post(self, request, session_id):
        session = get_object_or_404(DiagnosticSession, id=session_id)
        result = DiagnosticService.complete_session(session=session, user=request.user)
        return Response(result)


class JourneyView(APIView):
    def get(self, request):
        from apps.couples.repositories import CoupleRepository
        couple = CoupleRepository.require_full_couple(request.user)
        data = JourneyService.get_journey_data(couple)
        data['i_am_partner_a'] = str(couple.partner_a_id) == str(request.user.id)
        return Response(data)
