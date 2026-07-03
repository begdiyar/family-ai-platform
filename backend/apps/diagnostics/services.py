import logging
from django.db import transaction
from django.utils import timezone

from shared.exceptions import BusinessLogicError, NotFoundError
from apps.users.models import User
from .models import DiagnosticSession, FamilyJourney, LevelProgress, DIAGNOSTIC_LEVELS
from .repositories import QuestionRepository, DiagnosticRepository, JourneyRepository

logger = logging.getLogger(__name__)


class DiagnosticService:

    @staticmethod
    def start_session(user: User, level_number: int = 1) -> DiagnosticSession:
        from apps.couples.repositories import CoupleRepository
        couple = CoupleRepository.require_full_couple(user)

        # Проверяем, что уровень разблокирован
        journey = JourneyRepository.get_for_couple(couple)
        if not journey:
            journey, _ = JourneyRepository.get_or_create(couple)

        if level_number > journey.max_unlocked_level:
            raise BusinessLogicError('LEVEL_LOCKED', f'Уровень {level_number} ещё не открыт')

        # Уже завершена?
        completed = DiagnosticRepository.get_completed_session(user, couple, level_number)
        if completed:
            raise BusinessLogicError('SESSION_ALREADY_COMPLETED', f'Диагностика уровня {level_number} уже завершена')

        # Уже в процессе?
        existing = DiagnosticRepository.get_active_session(user, couple, level_number)
        if existing:
            raise BusinessLogicError('SESSION_ALREADY_IN_PROGRESS', 'Сессия диагностики уже активна')

        return DiagnosticRepository.create_session(user=user, couple=couple, level_number=level_number)

    @staticmethod
    def get_current_session(user: User) -> DiagnosticSession:
        from apps.couples.repositories import CoupleRepository
        couple = CoupleRepository.require_full_couple(user)

        # Сначала ищем активную сессию
        session = DiagnosticRepository.get_any_active_session(user, couple)
        if session:
            return session

        # Потом последнюю завершённую
        journey = JourneyRepository.get_for_couple(couple)
        if journey:
            level = journey.max_unlocked_level
            session = DiagnosticRepository.get_completed_session(user, couple, level)
            if session:
                return session

        raise NotFoundError('NO_ACTIVE_SESSION', 'Нет активной сессии диагностики')

    @staticmethod
    def save_answers(session: DiagnosticSession, user: User, answers_data: list) -> dict:
        if str(session.user_id) != str(user.id):
            raise BusinessLogicError('FORBIDDEN', 'Нет доступа к этой сессии')
        saved = DiagnosticRepository.bulk_upsert_answers(session, answers_data)
        total = QuestionRepository.count_by_level(session.level_number)
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

        couple = session.couple
        level_number = session.level_number

        with transaction.atomic():
            DiagnosticRepository.mark_completed(session)

            # Обновляем LevelProgress для текущего уровня
            journey = JourneyRepository.get_for_couple(couple)
            if journey:
                lp, _ = LevelProgress.objects.get_or_create(journey=journey, level_number=level_number)
                if lp:
                    is_partner_a = str(couple.partner_a_id) == str(user.id)
                    if is_partner_a:
                        lp.partner_a_done = True
                    else:
                        lp.partner_b_done = True

                    partner_session = DiagnosticRepository.get_partner_session(session)
                    if partner_session:
                        lp.both_diagnosed_at = timezone.now()
                        lp.save(update_fields=['partner_a_done', 'partner_b_done', 'both_diagnosed_at', 'updated_at'])

                        # Запускаем аналитику
                        couple_id = str(couple.id)
                        transaction.on_commit(
                            lambda: _trigger_analytics(couple_id)
                        )

                        return {
                            'session_id': str(session.id),
                            'level_number': level_number,
                            'status': 'completed',
                            'partner_completed': True,
                            'message': 'Оба завершили! Анализируем результаты...',
                        }
                    else:
                        lp.save(update_fields=['partner_a_done', 'partner_b_done', 'updated_at'])

        return {
            'session_id': str(session.id),
            'level_number': level_number,
            'status': 'completed',
            'partner_completed': False,
            'message': 'Вы завершили! Ждём партнёра.',
        }


def _trigger_analytics(couple_id: str) -> None:
    try:
        from apps.analytics.tasks import calculate_analytics
        calculate_analytics.delay(couple_id)
    except Exception as e:
        logger.warning(f'Could not trigger analytics for couple {couple_id}: {e}')


class JourneyService:

    @staticmethod
    def get_or_create_journey(couple) -> FamilyJourney:
        journey, _ = JourneyRepository.get_or_create(couple)
        return journey

    @staticmethod
    def check_and_unlock_next_level(couple) -> bool:
        """
        Проверяет условия разблокировки следующего уровня.
        Условия: оба прошли диагностику текущего уровня + XP практик >= уровень.
        Возвращает True если новый уровень был разблокирован.
        """
        try:
            journey = JourneyRepository.get_for_couple(couple)
            if not journey:
                return False

            current_level = journey.max_unlocked_level
            lp = JourneyRepository.get_level_progress(journey, current_level)
            if not lp:
                return False

            # Оба должны пройти диагностику этого уровня
            if not lp.both_diagnosed_at:
                return False

            # Уже завершён?
            if lp.completed_at:
                return False

            # XP из практик должен соответствовать уровню
            try:
                from apps.practices.models import FamilyDevelopmentPlan
                plan = FamilyDevelopmentPlan.objects.filter(couple=couple).first()
                if not plan:
                    return False
                if plan.current_level < current_level:
                    return False
            except Exception:
                return False

            # Всё условие выполнено — разблокируем следующий уровень
            with transaction.atomic():
                lp.practices_done_at = timezone.now()
                lp.save(update_fields=['practices_done_at', 'updated_at'])

            JourneyRepository.unlock_next_level(journey, current_level)
            logger.info(f'Level {current_level + 1} unlocked for couple {couple.id}')
            return True

        except Exception as e:
            logger.warning(f'check_and_unlock_next_level failed: {e}')
            return False

    @staticmethod
    def get_journey_data(couple) -> dict:
        """Возвращает полные данные пути семьи для API."""
        journey = JourneyRepository.get_for_couple(couple)
        if not journey:
            journey = JourneyService.get_or_create_journey(couple)

        lp_map = {lp.level_number: lp for lp in journey.level_progress.all()}

        levels = []
        for num, title, emoji, desc in DIAGNOSTIC_LEVELS:
            lp = lp_map.get(num)
            if num > journey.max_unlocked_level:
                status = 'locked'
            elif lp:
                status = lp.status
            else:
                status = 'unlocked'

            levels.append({
                'level_number': num,
                'title': title,
                'emoji': emoji,
                'description': desc,
                'status': status,
                'partner_a_done': lp.partner_a_done if lp else False,
                'partner_b_done': lp.partner_b_done if lp else False,
                'both_diagnosed_at': lp.both_diagnosed_at.isoformat() if lp and lp.both_diagnosed_at else None,
                'completed_at': lp.completed_at.isoformat() if lp and lp.completed_at else None,
            })

        return {
            'max_unlocked_level': journey.max_unlocked_level,
            'last_completed_level': journey.last_completed_level,
            'levels': levels,
        }
