from django.db import transaction
from shared.exceptions import BusinessLogicError, NotFoundError
from apps.users.models import User
from .models import DiagnosticSession, Question
from .repositories import QuestionRepository, DiagnosticRepository


class DiagnosticService:
    @staticmethod
    def start_session(user: User) -> DiagnosticSession:
        couple = user.get_active_couple()
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Сначала привяжите партнёра')
        existing = DiagnosticRepository.get_active_session(user, couple)
        if existing:
            raise BusinessLogicError('SESSION_ALREADY_IN_PROGRESS', 'Сессия диагностики уже активна')
        completed = DiagnosticRepository.get_completed_session(user, couple)
        if completed:
            raise BusinessLogicError('SESSION_ALREADY_COMPLETED', 'Диагностика уже завершена')
        return DiagnosticRepository.create_session(user=user, couple=couple)

    @staticmethod
    def get_current_session(user: User) -> DiagnosticSession:
        couple = user.get_active_couple()
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        session = DiagnosticRepository.get_active_session(user, couple)
        if not session:
            session = DiagnosticRepository.get_completed_session(user, couple)
        if not session:
            raise NotFoundError('NO_ACTIVE_SESSION', 'Нет активной сессии диагностики')
        return session

    @staticmethod
    def save_answers(session: DiagnosticSession, user: User, answers_data: list) -> dict:
        if str(session.user_id) != str(user.id):
            raise BusinessLogicError('FORBIDDEN', 'Нет доступа к этой сессии')
        saved = DiagnosticRepository.bulk_upsert_answers(session, answers_data)
        total = QuestionRepository.count_active()
        count = DiagnosticRepository.get_answers_count(session)
        return {
            'saved': saved,
            'answers_count': count,
            'total_questions': total,
            'progress_percent': round(count / total * 100) if total else 0,
        }

    @staticmethod
    def complete_session(session: DiagnosticSession, user: User) -> dict:
        if str(session.user_id) != str(user.id):
            raise BusinessLogicError('FORBIDDEN', 'Нет доступа к этой сессии')

        with transaction.atomic():
            DiagnosticRepository.mark_completed(session)
            partner_session = DiagnosticRepository.get_partner_session(session)

            if partner_session:
                from apps.analytics.tasks import calculate_analytics
                couple_id = str(session.couple_id)
                transaction.on_commit(lambda: calculate_analytics.delay(couple_id))
                return {
                    'session_id': str(session.id),
                    'status': 'completed',
                    'partner_completed': True,
                    'message': 'Оба завершили. Результаты готовятся!',
                }

        return {
            'session_id': str(session.id),
            'status': 'completed',
            'partner_completed': False,
            'message': 'Ждём партнёра. Результаты появятся, когда оба завершат.',
        }
