from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from shared.utils import get_request_language
from .models import DailyPractice
from .serializers import DailyPracticeSerializer
from .services import DailyPracticeService


class TodayPracticeView(APIView):
    def get(self, request):
        lang = get_request_language(request)
        practice = DailyPracticeService.get_today(request.user, language=lang)
        completions = DailyPracticeService.get_completions(request.user, practice)
        return Response(
            DailyPracticeSerializer(practice, context={'completions': completions, 'language': lang}).data
        )


class CompletePracticeView(APIView):
    def post(self, request, practice_id):
        practice = get_object_or_404(DailyPractice, id=practice_id)
        field_name = request.data.get('field_name')
        DailyPracticeService.mark_complete(request.user, practice, field_name)
        return Response({'success': True}, status=status.HTTP_200_OK)
