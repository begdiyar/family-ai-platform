import datetime
from django.utils.timezone import now

from .repositories import (
    ArticleRepository, TrainingRepository, ProgramRepository,
    MicroPracticeRepository, AchievementRepository,
)
from .models import Achievement


class AcademyService:

    @staticmethod
    def get_recommendations(user):
        """
        Персональные рекомендации на основе аналитики пары.
        Если нет аналитики — возвращает стартовые материалы.
        """
        from apps.analytics.repositories import AnalyticsRepository
        from apps.couples.repositories import CoupleRepository

        recommendations = []
        completed_article_ids = ArticleRepository.get_completed_ids_for_user(user)
        training_progress = TrainingRepository.get_all_progress_for_user(user)

        couple = CoupleRepository.get_active_for_user(user)
        result = AnalyticsRepository.get_latest_for_couple(couple) if couple else None

        if result:
            from apps.analytics.services import AnalyticsService
            zone_details = AnalyticsService.get_zone_detail_for_result(result)
            low_zones = [z for z in zone_details if z['couple_avg'] < 50]

            for zone_detail in low_zones[:2]:
                zone = zone_detail['zone']
                articles = list(
                    ArticleRepository.list_published(category=zone)
                    .exclude(id__in=completed_article_ids)[:2]
                )
                for article in articles:
                    recommendations.append({
                        'type': 'article',
                        'reason': f'Укрепить зону «{zone_detail["label"]}»',
                        'item': article,
                    })

            if result.crisis_level in ('warning', 'critical'):
                trainings = list(
                    TrainingRepository.list_all()
                    .exclude(id__in=[k for k, v in training_progress.items() if v.status == 'completed'])
                    .filter(skill_type__in=['conflict_resolution', 'constructive_dialogue'])[:1]
                )
                for t in trainings:
                    recommendations.append({
                        'type': 'training',
                        'reason': 'Навыки конструктивного общения во время кризиса',
                        'item': t,
                    })

        if not recommendations:
            articles = list(
                ArticleRepository.list_published(category='communication')
                .exclude(id__in=completed_article_ids)[:3]
            )
            for article in articles:
                recommendations.append({
                    'type': 'article',
                    'reason': 'Хорошее начало для любой пары',
                    'item': article,
                })

        program = ProgramRepository.list_all().filter(duration_days=7).first()
        if program:
            enrollment = ProgramRepository.get_enrollment(user, program)
            if not enrollment:
                recommendations.append({
                    'type': 'program',
                    'reason': 'Программа для старта — 7 дней улучшения общения',
                    'item': program,
                })

        return recommendations[:5]

    @staticmethod
    def get_learning_progress(user):
        articles_read = ArticleRepository.count_completed(user)
        trainings_completed = TrainingRepository.count_completed(user)
        programs_completed = ProgramRepository.count_completed(user)
        streak = AcademyService._compute_streak(user)

        total_minutes = (
            articles_read * 7 +
            trainings_completed * 15 +
            programs_completed * 60
        )

        skills = AcademyService._compute_skills(user)

        return {
            'articles_read': articles_read,
            'trainings_completed': trainings_completed,
            'programs_completed': programs_completed,
            'current_streak': streak,
            'total_minutes': total_minutes,
            'skills': skills,
        }

    @staticmethod
    def _compute_skills(user):
        from .models import UserTrainingProgress, Training
        completed = UserTrainingProgress.objects.filter(
            user=user, status=UserTrainingProgress.STATUS_COMPLETED
        ).select_related('training')

        skill_labels = dict(Training.SKILL_CHOICES)
        skill_levels: dict[str, int] = {}
        for p in completed:
            skill_levels[p.training.skill_type] = skill_levels.get(p.training.skill_type, 0) + 1

        return [
            {'key': k, 'name': skill_labels.get(k, k), 'level': min(v, 3)}
            for k, v in skill_levels.items()
        ]

    @staticmethod
    def _compute_streak(user) -> int:
        from .models import UserMicroPracticeLog
        import datetime as dt
        dates = set(
            UserMicroPracticeLog.objects.filter(user=user).values_list('date', flat=True)
        )
        if not dates:
            return 0
        today = now().date()
        streak = 0
        for i in range(365):
            check = today - dt.timedelta(days=i)
            if check in dates:
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def check_and_award_achievements(user):
        all_achievements = list(AchievementRepository.get_all())
        earned_keys = AchievementRepository.get_earned_keys(user)
        newly_earned = []

        articles_read = ArticleRepository.count_completed(user)
        trainings_done = TrainingRepository.count_completed(user)
        programs_done = ProgramRepository.count_completed(user)
        streak = AcademyService._compute_streak(user)

        counters = {
            Achievement.CONDITION_ARTICLES: articles_read,
            Achievement.CONDITION_TRAININGS: trainings_done,
            Achievement.CONDITION_PROGRAMS: programs_done,
            Achievement.CONDITION_STREAK: streak,
        }

        for achievement in all_achievements:
            if achievement.key in earned_keys:
                continue
            current = counters.get(achievement.condition_type, 0)
            if current >= achievement.condition_value:
                AchievementRepository.award(user, achievement)
                newly_earned.append(achievement)

        return newly_earned
