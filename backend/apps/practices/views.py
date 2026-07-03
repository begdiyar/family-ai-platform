from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DailyAssignmentSerializer, FamilyDevelopmentPlanSerializer
from .services import PracticeService


def _lang(request) -> str:
    lang = (
        request.query_params.get('lang')
        or request.headers.get('X-Language')
        or getattr(request._request, 'LANGUAGE_CODE', None)
        or 'ru'
    )
    return lang if lang in ('ru', 'en', 'uz') else 'ru'


class TodayPracticeView(APIView):
    def get(self, request):
        result = PracticeService.get_today(request.user)

        # Diagnostics gate
        if isinstance(result, dict):
            couple = request.user.get_active_couple()
            if couple:
                result['i_am_partner_a'] = str(couple.partner_a_id) == str(request.user.id)
            return Response(result)

        assignment, plan = result
        return Response(
            DailyAssignmentSerializer(
                assignment,
                context={'lang': _lang(request), 'plan': plan},
            ).data
        )


class CompleteSlotView(APIView):
    def post(self, request, assignment_id, slot):
        result = PracticeService.complete_slot(request.user, str(assignment_id), slot)

        if isinstance(result, dict):
            return Response(result)

        assignment, plan = result
        return Response(
            DailyAssignmentSerializer(
                assignment,
                context={'lang': _lang(request), 'plan': plan},
            ).data
        )


class FamilyPlanView(APIView):
    def get(self, request):
        result = PracticeService.get_plan(request.user)

        if isinstance(result, dict):
            return Response(result)

        return Response(FamilyDevelopmentPlanSerializer(result).data)


class PracticeStatsView(APIView):
    def get(self, request):
        return Response(PracticeService.get_stats(request.user))


class PracticeHistoryView(APIView):
    def get(self, request):
        limit   = min(int(request.query_params.get('limit', 14)), 90)
        history = PracticeService.get_history(request.user, limit=limit)
        return Response(
            DailyAssignmentSerializer(
                history, many=True,
                context={'lang': _lang(request)},
            ).data
        )
