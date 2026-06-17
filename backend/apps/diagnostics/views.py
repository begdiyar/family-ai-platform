from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Question, DiagnosticSession
from .repositories import QuestionRepository
from .serializers import (
    ZoneQuestionsSerializer, SessionSerializer, SaveAnswersSerializer
)
from .services import DiagnosticService

ZONE_LABELS = {
    'communication': 'Коммуникация',
    'trust': 'Доверие',
    'intimacy': 'Близость',
    'conflict': 'Конфликты',
    'values': 'Ценности',
    'future': 'Будущее',
}


class QuestionsView(APIView):
    def get(self, request):
        questions = QuestionRepository.get_all_active()
        zones_data = []
        zones_order = ['communication', 'trust', 'intimacy', 'conflict', 'values', 'future']
        for zone in zones_order:
            zone_questions = [q for q in questions if q.zone == zone]
            if zone_questions:
                zones_data.append({
                    'zone': zone,
                    'label': ZONE_LABELS[zone],
                    'questions': zone_questions,
                })
        return Response({
            'total': len(questions),
            'zones': ZoneQuestionsSerializer(zones_data, many=True).data,
        })


class SessionCreateView(APIView):
    def post(self, request):
        session = DiagnosticService.start_session(request.user)
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
