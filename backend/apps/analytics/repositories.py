from typing import Optional, List
from .models import AnalyticsResult, ZoneScore
from apps.couples.models import Couple


class AnalyticsRepository:
    @staticmethod
    def get_latest_for_couple(couple: Couple) -> Optional[AnalyticsResult]:
        return (
            AnalyticsResult.objects
            .filter(couple=couple)
            .select_related('session_a', 'session_b')
            .prefetch_related('zone_scores__user')
            .order_by('-created_at')
            .first()
        )

    @staticmethod
    def get_by_id(result_id) -> Optional[AnalyticsResult]:
        return (
            AnalyticsResult.objects
            .filter(id=result_id)
            .select_related('session_a', 'session_b')
            .prefetch_related('zone_scores__user')
            .first()
        )

    @staticmethod
    def list_for_couple(couple: Couple) -> List[AnalyticsResult]:
        return list(
            AnalyticsResult.objects
            .filter(couple=couple)
            .select_related('session_a', 'session_b')
            .order_by('-created_at')
        )

    @staticmethod
    def create(couple, session_a, session_b, overall_score, key_insights) -> AnalyticsResult:
        return AnalyticsResult.objects.create(
            couple=couple,
            session_a=session_a,
            session_b=session_b,
            overall_score=overall_score,
            key_insights=key_insights,
        )

    @staticmethod
    def bulk_create_zone_scores(result: AnalyticsResult, scores: list) -> None:
        ZoneScore.objects.bulk_create([
            ZoneScore(
                result=result,
                zone=s['zone'],
                user_id=s['user_id'],
                score=s['score'],
                max_score=s['max_score'],
            )
            for s in scores
        ])

    @staticmethod
    def get_insight_for_result(result: AnalyticsResult):
        from .models import AnalyticsInsight
        return AnalyticsInsight.objects.filter(analytics_result=result).first()

    @staticmethod
    def update_insights(result: AnalyticsResult, insights: list) -> None:
        result.key_insights = insights
        result.save(update_fields=['key_insights', 'updated_at'])

    @staticmethod
    def get_previous_for_couple(couple: Couple, exclude_id) -> Optional[AnalyticsResult]:
        return (
            AnalyticsResult.objects
            .filter(couple=couple)
            .exclude(id=exclude_id)
            .select_related('session_a', 'session_b')
            .prefetch_related('zone_scores__user')
            .order_by('-created_at')
            .first()
        )

    @staticmethod
    def get_history_for_couple(couple: Couple) -> List[AnalyticsResult]:
        return list(
            AnalyticsResult.objects
            .filter(couple=couple)
            .select_related('session_a', 'session_b')
            .prefetch_related('zone_scores')
            .order_by('created_at')
        )
