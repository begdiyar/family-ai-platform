import json
import logging
from apps.users.models import User
from apps.couples.repositories import CoupleRepository
from shared.exceptions import BusinessLogicError, NotFoundError
from .models import ConflictSession, ConflictEntry

logger = logging.getLogger(__name__)


class MediationService:
    @staticmethod
    def create_session(user: User, title: str) -> ConflictSession:
        couple = CoupleRepository.require_full_couple(user)
        return ConflictSession.objects.create(couple=couple, title=title)

    @staticmethod
    def submit_entry(session: ConflictSession, user: User, description: str,
                     feelings: str = '', desired_outcome: str = '') -> ConflictEntry:
        if str(session.couple.partner_a_id) != str(user.id) and \
                str(session.couple.partner_b_id) != str(user.id):
            raise BusinessLogicError('FORBIDDEN', 'Нет доступа к этой сессии')
        if session.status == ConflictSession.STATUS_COMPLETE:
            raise BusinessLogicError('SESSION_CLOSED', 'Сессия уже завершена')

        entry, _ = ConflictEntry.objects.update_or_create(
            session=session, user=user,
            defaults={'description': description, 'feelings': feelings, 'desired_outcome': desired_outcome},
        )

        if session.both_submitted() and session.status == ConflictSession.STATUS_COLLECTING:
            session.status = ConflictSession.STATUS_ANALYZING
            session.save(update_fields=['status'])
            from .tasks import analyze_conflict
            analyze_conflict.delay(str(session.id))

        return entry

    @staticmethod
    def analyze(session: ConflictSession) -> dict:
        try:
            from apps.ai_consultant.providers import AIProviderFactory
            entries = list(session.entries.select_related('user').all())
            if len(entries) < 2:
                raise ValueError('Нужно два участника')

            couple = session.couple
            name_a = couple.partner_a.first_name
            name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            def get_entry(name):
                for e in entries:
                    if e.user.first_name == name:
                        return e
                return entries[0]

            entry_a = get_entry(name_a)
            entry_b = get_entry(name_b)

            prompt = f"""Ты нейтральный семейный медиатор. Проведи анализ конфликта между {name_a} и {name_b}.

Тема конфликта: {session.title}

Описание ситуации от {name_a}:
"{entry_a.description}"
Чувства {name_a}: "{entry_a.feelings}"
Желаемый исход для {name_a}: "{entry_a.desired_outcome}"

Описание ситуации от {name_b}:
"{entry_b.description}"
Чувства {name_b}: "{entry_b.feelings}"
Желаемый исход для {name_b}: "{entry_b.desired_outcome}"

ВАЖНО: Будь полностью нейтральным. Не вставай ни на чью сторону.

Верни JSON:
{{
  "partner_a_position": "Позиция {name_a} своими словами, без осуждения (2-3 предложения)",
  "partner_b_position": "Позиция {name_b} своими словами, без осуждения (2-3 предложения)",
  "common_interests": ["Общий интерес 1", "Общий интерес 2"],
  "conflict_points": ["Точка конфликта 1", "Точка конфликта 2"],
  "compromises": [
    {{"title": "Вариант компромисса 1", "description": "Краткое описание"}},
    {{"title": "Вариант компромисса 2", "description": "Краткое описание"}}
  ],
  "first_step": "Один конкретный первый шаг для обоих (1 предложение)"
}}"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Ты медиатор. Отвечай только на русском. Только валидный JSON.'},
                {'role': 'user', 'content': prompt},
            ])
            start, end = response.find('{'), response.rfind('}') + 1
            if start >= 0 and end > start:
                analysis = json.loads(response[start:end])
                session.ai_analysis = analysis
                session.status = ConflictSession.STATUS_COMPLETE
                session.save(update_fields=['ai_analysis', 'status'])
                return analysis
        except Exception as e:
            logger.error(f"Conflict analysis failed for session {session.id}: {e}")
            session.status = ConflictSession.STATUS_COLLECTING
            session.save(update_fields=['status'])
        return {}
