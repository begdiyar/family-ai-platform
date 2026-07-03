from django.utils import timezone
from typing import Optional, List

from .models import Question, DiagnosticSession, Answer, FamilyJourney, LevelProgress
from apps.couples.models import Couple
from apps.users.models import User


class QuestionRepository:
    @staticmethod
    def get_by_level(level_number: int) -> List[Question]:
        return list(
            Question.objects
            .filter(level_number=level_number, is_active=True)
            .order_by('zone', 'order_index')
        )

    @staticmethod
    def count_by_level(level_number: int) -> int:
        return Question.objects.filter(level_number=level_number, is_active=True).count()

    @staticmethod
    def get_all_active() -> List[Question]:
        return list(Question.objects.filter(is_active=True).order_by('level_number', 'zone', 'order_index'))

    @staticmethod
    def count_active() -> int:
        return Question.objects.filter(is_active=True).count()


class DiagnosticRepository:
    @staticmethod
    def get_active_session(user: User, couple: Couple, level_number: int) -> Optional[DiagnosticSession]:
        return DiagnosticSession.objects.filter(
            user=user,
            couple=couple,
            level_number=level_number,
            status=DiagnosticSession.STATUS_IN_PROGRESS,
        ).first()

    @staticmethod
    def get_completed_session(user: User, couple: Couple, level_number: int) -> Optional[DiagnosticSession]:
        return DiagnosticSession.objects.filter(
            user=user,
            couple=couple,
            level_number=level_number,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).first()

    @staticmethod
    def get_any_active_session(user: User, couple: Couple) -> Optional[DiagnosticSession]:
        """Найти любую активную сессию (для уточнения текущего уровня)."""
        return DiagnosticSession.objects.filter(
            user=user,
            couple=couple,
            status=DiagnosticSession.STATUS_IN_PROGRESS,
        ).order_by('-level_number').first()

    @staticmethod
    def get_partner_session(session: DiagnosticSession) -> Optional[DiagnosticSession]:
        return DiagnosticSession.objects.filter(
            couple=session.couple,
            level_number=session.level_number,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).exclude(user=session.user).first()

    @staticmethod
    def create_session(user: User, couple: Couple, level_number: int) -> DiagnosticSession:
        return DiagnosticSession.objects.create(
            user=user,
            couple=couple,
            level_number=level_number,
        )

    @staticmethod
    def mark_completed(session: DiagnosticSession) -> None:
        session.status = DiagnosticSession.STATUS_COMPLETED
        session.finished_at = timezone.now()
        session.save(update_fields=['status', 'finished_at', 'updated_at'])

    @staticmethod
    def get_answers_count(session: DiagnosticSession) -> int:
        return Answer.objects.filter(session=session).count()

    @staticmethod
    def bulk_upsert_answers(session: DiagnosticSession, answers_data: list) -> int:
        saved = 0
        for item in answers_data:
            question_id = item.get('question_id')
            Answer.objects.update_or_create(
                session=session,
                question_id=question_id,
                defaults={
                    'user': session.user,
                    'value_scale': item.get('value_scale'),
                    'value_choice': item.get('value_choice'),
                    'value_text': item.get('value_text'),
                },
            )
            saved += 1
        return saved

    @staticmethod
    def get_all_completed_sessions_for_user(user: User, couple: Couple) -> List[DiagnosticSession]:
        """Все завершённые сессии пользователя в паре (все уровни)."""
        return list(
            DiagnosticSession.objects.filter(
                user=user,
                couple=couple,
                status=DiagnosticSession.STATUS_COMPLETED,
            ).order_by('level_number')
        )

    @staticmethod
    def get_both_completed_sessions_for_level(couple: Couple, level_number: int):
        """Обе сессии для конкретного уровня (для аналитики)."""
        sessions = list(DiagnosticSession.objects.filter(
            couple=couple,
            level_number=level_number,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).select_related('user'))
        if len(sessions) >= 2:
            return sessions
        return None

    @staticmethod
    def get_couple_completion_status(couple: Couple, level_number: int) -> dict:
        sessions = DiagnosticSession.objects.filter(
            couple=couple,
            level_number=level_number,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).values_list('user_id', flat=True)
        completed_ids = set(str(uid) for uid in sessions)
        return {
            'partner_a_completed': str(couple.partner_a_id) in completed_ids,
            'partner_b_completed': str(couple.partner_b_id) in completed_ids if couple.partner_b_id else False,
        }


class JourneyRepository:
    @staticmethod
    def get_or_create(couple: Couple) -> tuple:
        journey, created = FamilyJourney.objects.get_or_create(couple=couple)
        if created:
            LevelProgress.objects.create(journey=journey, level_number=1)
        return journey, created

    @staticmethod
    def get_for_couple(couple: Couple) -> Optional[FamilyJourney]:
        return FamilyJourney.objects.filter(couple=couple).prefetch_related('level_progress').first()

    @staticmethod
    def get_level_progress(journey: FamilyJourney, level_number: int) -> Optional[LevelProgress]:
        return LevelProgress.objects.filter(journey=journey, level_number=level_number).first()

    @staticmethod
    def unlock_next_level(journey: FamilyJourney, completed_level: int) -> Optional[LevelProgress]:
        from django.db import transaction
        with transaction.atomic():
            lp = LevelProgress.objects.filter(
                journey=journey, level_number=completed_level
            ).first()
            if lp and not lp.completed_at:
                lp.completed_at = timezone.now()
                lp.save(update_fields=['completed_at', 'updated_at'])

            journey.last_completed_level = completed_level
            next_level = completed_level + 1

            if next_level <= 10:
                journey.max_unlocked_level = max(journey.max_unlocked_level, next_level)
                journey.save(update_fields=['max_unlocked_level', 'last_completed_level', 'updated_at'])
                new_lp, _ = LevelProgress.objects.get_or_create(
                    journey=journey,
                    level_number=next_level,
                )
                return new_lp
            else:
                journey.save(update_fields=['last_completed_level', 'updated_at'])
                return None


class AnswerRepository:
    @staticmethod
    def get_by_session_and_zone(session: DiagnosticSession, zone: str) -> List[Answer]:
        return list(
            Answer.objects
            .filter(session=session, question__zone=zone)
            .select_related('question')
        )

    @staticmethod
    def get_by_sessions_and_zone(sessions, zone: str) -> List[Answer]:
        """Ответы по зоне из множества сессий (для кумулятивной аналитики)."""
        return list(
            Answer.objects
            .filter(session__in=sessions, question__zone=zone)
            .select_related('question')
        )
