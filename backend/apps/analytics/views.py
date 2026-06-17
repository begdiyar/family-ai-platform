from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from shared.exceptions import NotFoundError
from apps.couples.repositories import CoupleRepository
from .models import AnalyticsResult
from .repositories import AnalyticsRepository
from .serializers import (
    AnalyticsResultShortSerializer,
    AnalyticsResultDetailSerializer,
    ProgressHistorySerializer,
)


class AnalyticsResultListView(APIView):
    def get(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        results = AnalyticsRepository.list_for_couple(couple)
        latest_id = str(results[0].id) if results else None
        serializer = AnalyticsResultShortSerializer(
            results, many=True, context={'latest_id': latest_id}
        )
        return Response({'count': len(results), 'results': serializer.data})


class AnalyticsResultLatestView(APIView):
    def get(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        result = AnalyticsRepository.get_latest_for_couple(couple)
        if not result:
            raise NotFoundError('NO_RESULTS_YET', 'Результаты диагностики ещё не готовы')
        return Response(AnalyticsResultDetailSerializer(result).data)


class AnalyticsResultDetailView(APIView):
    def get(self, request, result_id):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        result = get_object_or_404(AnalyticsResult, id=result_id, couple=couple)
        return Response(AnalyticsResultDetailSerializer(result).data)


class AnalyticsProgressView(APIView):
    def get(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        history = AnalyticsRepository.get_history_for_couple(couple)
        return Response({
            'zones': ['communication', 'trust', 'intimacy', 'conflict', 'values', 'future'],
            'history': ProgressHistorySerializer(history, many=True).data,
        })
