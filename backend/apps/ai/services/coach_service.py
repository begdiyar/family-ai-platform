import logging

from apps.ai.context_builder.builder import ContextBuilder, CoupleContext
from apps.ai.providers.factory import AIProviderFactory

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты — AI-консультант по семейным отношениям «Связь». \
Помогаешь парам улучшать отношения с помощью методов доказательной психологии: \
CBT (когнитивно-поведенческая терапия), EFT (эмоционально-фокусированная терапия) и метода Готтмана.

Принципы работы:
• Эмпатичен, не осуждаешь, тёплый и поддерживающий тон
• Никогда не ставишь диагнозы и не упоминаешь патологии
• Используешь «зона роста» вместо «проблема»
• При признаках насилия или кризиса безопасности — обязательно рекомендуй специалиста
• Отвечаешь только на русском языке
• Задаёшь уточняющие вопросы, а не даёшь готовые рецепты
• Максимум 300 слов в ответе
• Опираешься на данные диагностики пары, если они предоставлены

Контекст пары будет добавлен ниже — используй его для персонализированных ответов."""

ZONE_STATUS_RU = {
    'strong':    'сильная зона',
    'growth':    'зона роста',
    'attention': 'требует внимания',
}


class CoachService:
    HISTORY_LIMIT = 20

    def __init__(self):
        self.provider = AIProviderFactory.get()

    # ── Public API ────────────────────────────────────────────────────────

    def chat(self, user, message: str, conversation_id: str = None) -> dict:
        from apps.ai_consultant.models import AIConversation, AIMessage
        from apps.ai_consultant.repositories import AIConversationRepository, AIMessageRepository

        from apps.couples.repositories import CoupleRepository
        couple       = CoupleRepository.require_full_couple(user)
        conversation = self._get_or_create_conversation(
            user, couple, conversation_id,
            AIConversationRepository, AIConversation,
        )

        AIMessageRepository.create(
            conversation, role=AIMessage.ROLE_USER, content=message,
        )

        messages      = self._build_messages(conversation, user, couple)
        response_text = self.provider.generate(messages)

        AIMessageRepository.create(
            conversation, role=AIMessage.ROLE_ASSISTANT, content=response_text,
        )

        return {
            'response':        response_text,
            'conversation_id': str(conversation.id),
        }

    # ── Private helpers ───────────────────────────────────────────────────

    def _get_or_create_conversation(self, user, couple, conversation_id, repo, model):
        if conversation_id:
            conv = repo.get_by_id(conversation_id, user)
            if conv:
                return conv
        return repo.create(
            couple      = couple,
            user        = user,
            dialog_type = model.DIALOG_COACH,
        )

    def _build_messages(self, conversation, user, couple) -> list:
        from apps.ai_consultant.repositories import AIMessageRepository

        ctx = ContextBuilder.build(couple)
        system_prompt = self._build_system_prompt(user, ctx)

        history = AIMessageRepository.get_recent(conversation, limit=self.HISTORY_LIMIT)

        messages = [{'role': 'system', 'content': system_prompt}]
        for msg in history:
            messages.append({'role': msg.role, 'content': msg.content})
        return messages

    def _build_system_prompt(self, user, ctx: CoupleContext) -> str:
        prompt = SYSTEM_PROMPT

        if not ctx.partner_a_name:
            return prompt

        _CONFLICT = {
            'avoidant': 'избегающий', 'confrontational': 'конфронтационный',
            'collaborative': 'совместное решение', 'competitive': 'соревновательный',
            'compromising': 'компромисс',
        }
        _SUPPORT = {
            'advice': 'советы и решения', 'empathy': 'сочувствие и понимание',
            'practical': 'практическая помощь', 'space': 'пространство для осмысления',
        }
        _REL_STATUS = {
            'dating': 'встречаемся', 'engaged': 'помолвлены',
            'cohabitating': 'живём вместе', 'married': 'женаты/замужем',
            'separated': 'живём раздельно',
        }
        _FV = {
            'respect': 'уважение', 'trust': 'доверие', 'love': 'любовь',
            'children': 'дети', 'education': 'образование',
            'financial_stability': 'финансовая стабильность', 'career': 'карьера',
            'faith': 'вера', 'traditions': 'традиции', 'travel': 'путешествия',
            'self_development': 'саморазвитие', 'health': 'здоровье',
        }

        is_a = (user.first_name == ctx.partner_a_name)
        partner_name = ctx.partner_b_name if is_a else ctx.partner_a_name
        my_age       = ctx.partner_a_age if is_a else ctx.partner_b_age
        my_occ       = ctx.partner_a_occupation if is_a else ctx.partner_b_occupation
        my_conflict  = ctx.partner_a_conflict_style if is_a else ctx.partner_b_conflict_style
        my_support   = ctx.partner_a_support_style if is_a else ctx.partner_b_support_style
        pt_conflict  = ctx.partner_b_conflict_style if is_a else ctx.partner_a_conflict_style
        pt_support   = ctx.partner_b_support_style if is_a else ctx.partner_a_support_style

        user_desc = user.first_name
        if my_age:
            user_desc += f' ({my_age} лет)'
        if my_occ:
            user_desc += f', {my_occ}'
        prompt += f'\n\nТы разговариваешь с {user_desc}. Их партнёр — {partner_name}.'

        # Стили общения
        if my_conflict or my_support:
            parts = []
            if my_conflict:
                parts.append(f'в конфликтах — {_CONFLICT.get(my_conflict, my_conflict)}')
            if my_support:
                parts.append(f'поддержку принимает как {_SUPPORT.get(my_support, my_support)}')
            prompt += f'\n{user.first_name}: {"; ".join(parts)}.'
        if pt_conflict or pt_support:
            parts = []
            if pt_conflict:
                parts.append(f'в конфликтах — {_CONFLICT.get(pt_conflict, pt_conflict)}')
            if pt_support:
                parts.append(f'поддержку принимает как {_SUPPORT.get(pt_support, pt_support)}')
            prompt += f'\n{partner_name}: {"; ".join(parts)}.'

        # Отношения
        rel_parts = []
        if ctx.relationship_status:
            rel_parts.append(_REL_STATUS.get(ctx.relationship_status, ctx.relationship_status))
        if ctx.relationship_years is not None:
            rel_parts.append(f'{ctx.relationship_years} лет вместе')
        if ctx.marriage_years is not None:
            rel_parts.append(f'в браке {ctx.marriage_years} лет')
        if rel_parts:
            prompt += f'\nОтношения: {", ".join(rel_parts)}.'

        if ctx.lives_with_parents:
            prompt += '\nЖивут с родителями / родственниками.'
        if ctx.relatives_influence_level:
            prompt += f'\nВлияние родственников: {ctx.relatives_influence_level}/5.'
        if ctx.religious_traditions_importance:
            prompt += f'\nЗначимость религиозных традиций: {ctx.religious_traditions_importance}/5.'

        if ctx.children:
            prompt += f'\nДетей: {len(ctx.children)}.'

        if ctx.couple_family_values:
            fv_ru = [_FV.get(s, s) for s in ctx.couple_family_values]
            prompt += f'\nСемейные ценности пары: {", ".join(fv_ru)}.'

        if ctx.relationship_index is not None:
            if ctx.crisis_level == 'critical':
                prompt += (
                    f'\n\n⚠️ КРИТИЧНО: Общий индекс пары — {ctx.relationship_index}/100. '
                    'Будь особенно бережным и поддерживающим.'
                )
            elif ctx.crisis_level == 'warning':
                prompt += f'\n\nОбщий индекс пары: {ctx.relationship_index}/100 (требует внимания).'
            else:
                prompt += f'\n\nОбщий индекс пары: {ctx.relationship_index}/100.'

        if ctx.zones:
            prompt += '\n\nПоказатели по зонам:'
            for z in ctx.zones:
                status = ZONE_STATUS_RU.get(z['status'], z['status'])
                prompt += (
                    f'\n• {z["label"]}: {round(z["couple_avg"])}% '
                    f'({status}, разрыв {round(z["gap"])}%)'
                )

        if ctx.family_level:
            prompt += f'\n\nТекущий уровень семейного развития: {ctx.family_level}/10.'

        if ctx.strengths:
            headline  = ctx.strengths.get('headline', '')
            strengths = ctx.strengths.get('strengths', [])
            if headline:
                prompt += f'\n\nСильные стороны пары: {headline}.'
            if strengths:
                prompt += f' Конкретно: {", ".join(strengths[:3])}.'

        if ctx.problem_chain:
            root = ctx.problem_chain[0]
            prompt += f'\n\nКорневая сложность: {root.get("problem", "")}.'

        if ctx.completed_practices:
            prompt += f'\n\nПрактики пары за последние 7 дней: {", ".join(ctx.completed_practices[:3])}.'

        if ctx.family_values:
            prompt += f'\n\nЦенности семьи: {", ".join(ctx.family_values[:3])}.'
        if ctx.communication_rules:
            prompt += f' Правила общения: {ctx.communication_rules[0]}.'

        return prompt
