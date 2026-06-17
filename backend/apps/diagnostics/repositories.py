from django.utils import timezone
from typing import Optional, List

from .models import Question, DiagnosticSession, Answer
from apps.couples.models import Couple
from apps.users.models import User


class QuestionRepository:
    @staticmethod
    def get_all_active() -> List[Question]:
        return list(Question.objects.filter(is_active=True).order_by('zone', 'order_index'))

    @staticmethod
    def get_by_zone(zone: str) -> List[Question]:
        return list(Question.objects.filter(zone=zone, is_active=True).order_by('order_index'))

    @staticmethod
    def count_active() -> int:
        return Question.objects.filter(is_active=True).count()


class DiagnosticRepository:
    @staticmethod
    def get_active_session(user: User, couple: Couple) -> Optional[DiagnosticSession]:
        return DiagnosticSession.objects.filter(
            user=user,
            couple=couple,
            status=DiagnosticSession.STATUS_IN_PROGRESS,
        ).first()

    @staticmethod
    def get_completed_session(user: User, couple: Couple) -> Optional[DiagnosticSession]:
        return DiagnosticSession.objects.filter(
            user=user,
            couple=couple,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).first()

    @staticmethod
    def get_partner_session(session: DiagnosticSession) -> Optional[DiagnosticSession]:
        return DiagnosticSession.objects.filter(
            couple=session.couple,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).exclude(user=session.user).first()

    @staticmethod
    def create_session(user: User, couple: Couple) -> DiagnosticSession:
        return DiagnosticSession.objects.create(user=user, couple=couple)

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
    def get_couple_completion_status(couple: Couple) -> dict:
        sessions = DiagnosticSession.objects.filter(
            couple=couple,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).values_list('user_id', flat=True)
        completed_ids = set(str(uid) for uid in sessions)
        return {
            'partner_a_completed': str(couple.partner_a_id) in completed_ids,
            'partner_b_completed': str(couple.partner_b_id) in completed_ids if couple.partner_b_id else False,
        }

    @staticmethod
    def get_both_completed_sessions(couple: Couple):
        sessions = DiagnosticSession.objects.filter(
            couple=couple,
            status=DiagnosticSession.STATUS_COMPLETED,
        ).select_related('user').order_by('finished_at')
        if sessions.count() >= 2:
            return list(sessions[:2])
        return None


class AnswerRepository:
    @staticmethod
    def get_by_session_and_zone(session: DiagnosticSession, zone: str) -> List[Answer]:
        return list(
            Answer.objects
            .filter(session=session, question__zone=zone)
            .select_related('question')
        )
