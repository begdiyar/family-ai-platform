import json
import logging
from apps.users.models import User
from apps.couples.repositories import CoupleRepository
from shared.exceptions import BusinessLogicError, NotFoundError
from .models import FamilyConstitution

logger = logging.getLogger(__name__)


class ConstitutionService:
    @staticmethod
    def get_or_create(user: User) -> FamilyConstitution:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')
        constitution, _ = FamilyConstitution.objects.get_or_create(couple=couple)
        return constitution

    @staticmethod
    def update(user: User, data: dict) -> FamilyConstitution:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')
        constitution, _ = FamilyConstitution.objects.get_or_create(couple=couple)
        allowed_fields = ['values', 'goals', 'communication_rules', 'conflict_rules',
                          'finance_principles', 'parenting_approach']
        for field in allowed_fields:
            if field in data:
                setattr(constitution, field, data[field])
        constitution.is_ai_generated = False
        constitution.save()
        return constitution

    @staticmethod
    def generate_with_ai(user: User) -> FamilyConstitution:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')

        name_a = couple.partner_a.first_name
        name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

        context = ""
        from apps.analytics.repositories import AnalyticsRepository
        result = AnalyticsRepository.get_latest_for_couple(couple)
        if result:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(result)
            strong = [z['label'] for z in zones if z['status'] == 'strong']
            attention = [z['label'] for z in zones if z['status'] == 'attention']
            if strong:
                context += f"\nСильные стороны пары: {', '.join(strong)}"
            if attention:
                context += f"\nЗоны роста: {', '.join(attention)}"

        has_children = couple.has_children

        prompt = f"""Помоги семье {name_a} и {name_b} создать их семейную конституцию.{context}
{"Есть дети." if has_children else "Детей нет."}

Создай документ с конкретными, живыми формулировками (не шаблонными).
Каждый пункт — конкретное правило или ценность, написанное от первого лица множественного числа.

Верни JSON:
{{
  "values": ["Ценность 1", "Ценность 2", "Ценность 3", "Ценность 4", "Ценность 5"],
  "goals": ["Цель 1", "Цель 2", "Цель 3"],
  "communication_rules": ["Правило общения 1", "Правило общения 2", "Правило общения 3"],
  "conflict_rules": ["Правило конфликта 1", "Правило конфликта 2", "Правило конфликта 3"],
  "finance_principles": ["Финансовый принцип 1", "Финансовый принцип 2"],
  "parenting_approach": {f'["Подход к детям 1", "Подход к детям 2"]' if has_children else '[]'}
}}"""

        try:
            from apps.ai_consultant.providers import AIProviderFactory
            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Отвечай только на русском. Только валидный JSON.'},
                {'role': 'user', 'content': prompt},
            ])
            start, end = response.find('{'), response.rfind('}') + 1
            if start >= 0 and end > start:
                data = json.loads(response[start:end])
                constitution, _ = FamilyConstitution.objects.get_or_create(couple=couple)
                for field in ['values', 'goals', 'communication_rules', 'conflict_rules',
                              'finance_principles', 'parenting_approach']:
                    if field in data:
                        setattr(constitution, field, data[field])
                constitution.is_ai_generated = True
                constitution.save()
                return constitution
        except Exception as e:
            logger.error(f"Constitution AI generation failed: {e}")
            raise BusinessLogicError('AI_FAILED', 'Не удалось сгенерировать конституцию')

        raise BusinessLogicError('AI_FAILED', 'Не удалось сгенерировать конституцию')
