from typing import Optional
from django.utils import timezone
from django.db.models import Prefetch

from .models import (
    Article, Training, Program, ProgramDay, AcademyMicroPractice,
    UserArticleProgress, UserTrainingProgress, UserProgramEnrollment,
    UserProgramDayProgress, UserMicroPracticeLog, Achievement, UserAchievement,
)


class ArticleRepository:
    @staticmethod
    def list_published(category: str = None, difficulty: str = None, search: str = None):
        qs = Article.objects.filter(is_published=True).prefetch_related('sources')
        if category:
            qs = qs.filter(category=category)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Article]:
        return Article.objects.filter(slug=slug, is_published=True).prefetch_related('sources').first()

    @staticmethod
    def get_completed_ids_for_user(user) -> set:
        return set(
            str(pid) for pid in
            UserArticleProgress.objects.filter(user=user).values_list('article_id', flat=True)
        )

    @staticmethod
    def mark_complete(user, article: Article) -> bool:
        obj, created = UserArticleProgress.objects.get_or_create(user=user, article=article)
        return created

    @staticmethod
    def count_completed(user) -> int:
        return UserArticleProgress.objects.filter(user=user).count()


class TrainingRepository:
    @staticmethod
    def list_all():
        return Training.objects.all()

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Training]:
        return Training.objects.filter(slug=slug).first()

    @staticmethod
    def get_progress(user, training: Training) -> Optional[UserTrainingProgress]:
        return UserTrainingProgress.objects.filter(user=user, training=training).first()

    @staticmethod
    def get_all_progress_for_user(user) -> dict:
        return {
            str(p.training_id): p
            for p in UserTrainingProgress.objects.filter(user=user)
        }

    @staticmethod
    def start_or_get(user, training: Training) -> tuple[UserTrainingProgress, bool]:
        return UserTrainingProgress.objects.get_or_create(
            user=user, training=training,
            defaults={'status': UserTrainingProgress.STATUS_STARTED}
        )

    @staticmethod
    def complete(user, training: Training, reflection_note: str = None) -> UserTrainingProgress:
        progress, _ = UserTrainingProgress.objects.get_or_create(user=user, training=training)
        progress.status = UserTrainingProgress.STATUS_COMPLETED
        progress.reflection_note = reflection_note
        progress.completed_at = timezone.now()
        progress.save(update_fields=['status', 'reflection_note', 'completed_at', 'updated_at'])
        return progress

    @staticmethod
    def count_completed(user) -> int:
        return UserTrainingProgress.objects.filter(
            user=user, status=UserTrainingProgress.STATUS_COMPLETED
        ).count()


class ProgramRepository:
    @staticmethod
    def list_all():
        return Program.objects.all()

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Program]:
        return Program.objects.filter(slug=slug).prefetch_related('days').first()

    @staticmethod
    def get_enrollment(user, program: Program) -> Optional[UserProgramEnrollment]:
        return UserProgramEnrollment.objects.filter(user=user, program=program).first()

    @staticmethod
    def get_active_enrollment(user) -> Optional[UserProgramEnrollment]:
        return (
            UserProgramEnrollment.objects
            .filter(user=user, status=UserProgramEnrollment.STATUS_ACTIVE)
            .select_related('program')
            .first()
        )

    @staticmethod
    def enroll(user, program: Program) -> tuple[UserProgramEnrollment, bool]:
        return UserProgramEnrollment.objects.get_or_create(
            user=user, program=program,
            defaults={'status': UserProgramEnrollment.STATUS_ACTIVE, 'current_day': 1}
        )

    @staticmethod
    def get_completed_day_numbers(enrollment: UserProgramEnrollment) -> set:
        return set(
            UserProgramDayProgress.objects.filter(enrollment=enrollment)
            .values_list('day__day_number', flat=True)
        )

    @staticmethod
    def complete_day(enrollment: UserProgramEnrollment, day: ProgramDay, reflection: str = None):
        obj, created = UserProgramDayProgress.objects.get_or_create(
            enrollment=enrollment, day=day,
            defaults={'reflection': reflection}
        )
        if created:
            next_day = day.day_number + 1
            if next_day > enrollment.program.duration_days:
                enrollment.status = UserProgramEnrollment.STATUS_COMPLETED
                enrollment.current_day = enrollment.program.duration_days
            else:
                enrollment.current_day = next_day
            enrollment.save(update_fields=['status', 'current_day', 'updated_at'])
        return obj, created

    @staticmethod
    def count_completed(user) -> int:
        return UserProgramEnrollment.objects.filter(
            user=user, status=UserProgramEnrollment.STATUS_COMPLETED
        ).count()


class MicroPracticeRepository:
    @staticmethod
    def get_for_today(user, date):
        log = UserMicroPracticeLog.objects.filter(user=user, date=date).select_related('practice').first()
        if log:
            return log.practice, True

        completed_ids = UserMicroPracticeLog.objects.filter(user=user).values_list('practice_id', flat=True)
        practice = (
            AcademyMicroPractice.objects
            .filter(is_active=True)
            .exclude(id__in=completed_ids)
            .order_by('order_index')
            .first()
        )
        if not practice:
            practice = AcademyMicroPractice.objects.filter(is_active=True).order_by('order_index').first()

        return practice, False

    @staticmethod
    def complete(user, practice: AcademyMicroPractice, date) -> bool:
        _, created = UserMicroPracticeLog.objects.get_or_create(
            user=user, date=date,
            defaults={'practice': practice}
        )
        return created


class AchievementRepository:
    @staticmethod
    def get_all():
        return Achievement.objects.all()

    @staticmethod
    def get_earned_keys(user) -> set:
        return set(
            UserAchievement.objects.filter(user=user)
            .values_list('achievement__key', flat=True)
        )

    @staticmethod
    def get_user_achievements(user):
        return (
            UserAchievement.objects
            .filter(user=user)
            .select_related('achievement')
            .order_by('earned_at')
        )

    @staticmethod
    def award(user, achievement: Achievement) -> bool:
        _, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
        return created

    @staticmethod
    def compute_streak(user) -> int:
        from django.utils.timezone import now
        dates = set(
            UserMicroPracticeLog.objects.filter(user=user)
            .values_list('date', flat=True)
        )
        if not dates:
            return 0
        today = now().date()
        streak = 0
        current = today
        while current in dates:
            streak += 1
            current = current.replace(day=current.day - 1)
            try:
                import datetime
                current = today - datetime.timedelta(days=streak)
            except Exception:
                break
        return streak
