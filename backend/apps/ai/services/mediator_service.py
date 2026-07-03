import logging

from apps.ai.context_builder.builder import ContextBuilder
from apps.ai.providers.factory import AIProviderFactory

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты — беспристрастный медиатор конфликтов для пар «Связь». \
Твоя задача — помочь партнёрам найти взаимовыгодное решение, не принимая ничьей стороны.

Принципы:
• Абсолютная беспристрастность — ты не поддерживаешь ни одного из партнёров
• Помогаешь каждому быть услышанным
• Фокусируешь на интересах, а не позициях
• Ищешь точки соприкосновения
• При признаках насилия — немедленно рекомендуй специалиста
• Отвечаешь только на русском языке
• Максимум 300 слов в ответе"""


class MediatorService:

    def __init__(self):
        self.provider = AIProviderFactory.get()

    def analyze(self, user, description: str, conversation_id: str = None) -> dict:
        from apps.ai_consultant.models import AIConversation, AIMessage
        from apps.ai_consultant.repositories import AIConversationRepository, AIMessageRepository

        from apps.couples.repositories import CoupleRepository
        couple       = CoupleRepository.require_full_couple(user)
        conversation = self._get_or_create_conversation(
            user, couple, conversation_id,
            AIConversationRepository, AIConversation,
        )

        AIMessageRepository.create(
            conversation, role=AIMessage.ROLE_USER, content=description,
        )

        context = self._build_context(couple)
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT + context},
            {'role': 'user',   'content': description},
        ]
        response_text = self.provider.generate(messages)

        AIMessageRepository.create(
            conversation, role=AIMessage.ROLE_ASSISTANT, content=response_text,
        )

        return {
            'response':        response_text,
            'conversation_id': str(conversation.id),
        }

    # ── Helpers ────────────────────────────────────────────────────────

    def _get_or_create_conversation(self, user, couple, conversation_id, repo, model):
        if conversation_id:
            conv = repo.get_by_id(conversation_id, user)
            if conv:
                return conv
        return repo.create(
            couple      = couple,
            user        = user,
            dialog_type = model.DIALOG_MEDIATOR,
        )

    def _build_context(self, couple) -> str:
        ctx = ContextBuilder.build(couple)

        if not ctx.partner_a_name:
            return ''

        _CONFLICT = {
            'avoidant': 'избегающий', 'confrontational': 'конфронтационный',
            'collaborative': 'совместное решение', 'competitive': 'соревновательный',
            'compromising': 'компромисс',
        }
        _REL_STATUS = {
            'dating': 'встречаемся', 'engaged': 'помолвлены',
            'cohabitating': 'живём вместе', 'married': 'женаты/замужем',
            'separated': 'живём раздельно',
        }

        def _partner_desc(name, age, conflict):
            parts = [name]
            if age:
                parts.append(f'{age} лет')
            desc = ', '.join(parts)
            if conflict:
                desc += f' (конфликты: {_CONFLICT.get(conflict, conflict)})'
            return desc

        a_desc = _partner_desc(ctx.partner_a_name, ctx.partner_a_age, ctx.partner_a_conflict_style)
        b_desc = _partner_desc(ctx.partner_b_name, ctx.partner_b_age, ctx.partner_b_conflict_style)
        context = f'\n\nПартнёры: {a_desc} и {b_desc}.'

        # Отношения
        rel_parts = []
        if ctx.relationship_status:
            rel_parts.append(_REL_STATUS.get(ctx.relationship_status, ctx.relationship_status))
        if ctx.relationship_years is not None:
            rel_parts.append(f'{ctx.relationship_years} лет вместе')
        if rel_parts:
            context += f' {", ".join(rel_parts).capitalize()}.'

        if ctx.children:
            context += f' Детей: {len(ctx.children)}.'

        if ctx.lives_with_parents:
            context += ' Живут с родственниками.'
        if ctx.relatives_influence_level and ctx.relatives_influence_level >= 4:
            context += f' Высокое влияние родственников ({ctx.relatives_influence_level}/5).'

        if ctx.weak_zones:
            labels = ', '.join(z['label'] for z in ctx.weak_zones)
            context += f' Зоны, требующие внимания: {labels}.'

        if ctx.relationship_index is not None:
            context += f' Общий индекс отношений: {ctx.relationship_index}/100.'

        if ctx.crisis_level == 'critical':
            context += ' ⚠️ Критический уровень — будь особенно бережным.'

        return context
