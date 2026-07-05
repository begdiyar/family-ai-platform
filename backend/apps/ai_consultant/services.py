import logging
from typing import Generator
from apps.users.models import User
from apps.couples.models import Couple
from .models import AIConversation, AIMessage
from .repositories import AIConversationRepository, AIMessageRepository
from .providers import AIProviderFactory

logger = logging.getLogger(__name__)

ZONE_LABELS = {
    'communication': 'Коммуникация',
    'trust': 'Доверие',
    'intimacy': 'Близость',
    'conflict': 'Конфликты',
    'values': 'Ценности',
    'future': 'Будущее',
}

SYSTEM_PROMPT_BASE = """Ты — AI-консультант по отношениям по имени «Связь». \
Ты помогаешь парам улучшить их отношения с помощью методов доказательной психологии: \
CBT (когнитивно-поведенческая терапия), EFT (эмоционально-фокусированная терапия) и метода Готтмана.

Принципы работы:
- Ты эмпатичен, не осуждаешь, используешь тёплый и поддерживающий тон
- Никогда не ставишь диагнозы и не говоришь о патологиях
- Вместо слова «проблема» используешь «зона роста»
- При признаках насилия или кризиса безопасности — рекомендуешь обратиться к специалисту
- Отвечаешь на русском языке
- Задаёшь уточняющие вопросы, а не даёшь готовые решения
- Максимальная длина ответа — 300 слов"""


class AIConsultantService:
    HISTORY_LIMIT = 20

    @classmethod
    def create_conversation(cls, user: User, couple: Couple, topic: str = None) -> dict:
        conv = AIConversationRepository.create(couple=couple, user=user)
        greeting = cls._build_greeting(conv, topic)
        AIMessageRepository.create(conv, role=AIMessage.ROLE_ASSISTANT, content=greeting)
        return {'conversation': conv, 'greeting': greeting}

    @classmethod
    def stream_response(cls, conversation: AIConversation, user_message: str) -> Generator[str, None, None]:
        AIMessageRepository.create(conversation, role=AIMessage.ROLE_USER, content=user_message)
        messages = cls._build_messages(conversation, user_message)
        provider = AIProviderFactory.get()

        full_response = ''
        for chunk in provider.stream(messages):
            full_response += chunk
            yield chunk

        AIMessageRepository.create(conversation, role=AIMessage.ROLE_ASSISTANT, content=full_response)

    @classmethod
    def _build_messages(cls, conversation: AIConversation, new_message: str) -> list:
        system_prompt = cls._build_system_prompt(conversation)
        history = AIMessageRepository.get_recent(conversation, limit=cls.HISTORY_LIMIT)

        messages = [{'role': 'system', 'content': system_prompt}]
        for msg in history:
            if msg.content != new_message or msg.role != AIMessage.ROLE_USER:
                messages.append({'role': msg.role, 'content': msg.content})
        messages.append({'role': 'user', 'content': new_message})
        return messages

    @classmethod
    def _build_system_prompt(cls, conversation: AIConversation) -> str:
        from apps.ai.context_builder.builder import ContextBuilder

        couple    = conversation.couple
        user_name = conversation.user.first_name
        ctx       = ContextBuilder.build(couple)

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

        name_a        = ctx.partner_a_name or (couple.partner_a.first_name if couple else '')
        name_b        = ctx.partner_b_name or 'партнёр'
        is_a          = (user_name == name_a)
        partner_name  = name_b if is_a else name_a
        my_age        = ctx.partner_a_age if is_a else ctx.partner_b_age
        my_occ        = ctx.partner_a_occupation if is_a else ctx.partner_b_occupation
        my_conflict   = ctx.partner_a_conflict_style if is_a else ctx.partner_b_conflict_style
        my_support    = ctx.partner_a_support_style if is_a else ctx.partner_b_support_style
        pt_conflict   = ctx.partner_b_conflict_style if is_a else ctx.partner_a_conflict_style
        pt_support    = ctx.partner_b_support_style if is_a else ctx.partner_a_support_style

        user_desc = user_name
        if my_age:
            user_desc += f' ({my_age} лет)'
        if my_occ:
            user_desc += f', {my_occ}'

        prompt = SYSTEM_PROMPT_BASE
        prompt += f"\n\nТы разговариваешь с {user_desc}. Их партнёр — {partner_name}."

        if my_conflict or my_support:
            parts = []
            if my_conflict:
                parts.append(f'в конфликтах — {_CONFLICT.get(my_conflict, my_conflict)}')
            if my_support:
                parts.append(f'поддержку принимает как {_SUPPORT.get(my_support, my_support)}')
            prompt += f'\n{user_name}: {"; ".join(parts)}.'
        if pt_conflict or pt_support:
            parts = []
            if pt_conflict:
                parts.append(f'в конфликтах — {_CONFLICT.get(pt_conflict, pt_conflict)}')
            if pt_support:
                parts.append(f'поддержку принимает как {_SUPPORT.get(pt_support, pt_support)}')
            prompt += f'\n{partner_name}: {"; ".join(parts)}.'

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
                    f"\n\n⚠️ ВАЖНО: Общий балл пары {ctx.relationship_index}% — критический уровень. "
                    "Будь особенно бережным и поддерживающим."
                )
            elif ctx.crisis_level == 'warning':
                prompt += f"\n\nОбщий балл пары: {ctx.relationship_index}% (требует внимания)."
            else:
                prompt += f"\n\nОбщий балл пары: {ctx.relationship_index}%."

        if ctx.zones:
            status_text = {'strong': 'сильная', 'growth': 'зона роста', 'attention': 'требует внимания'}
            prompt += "\nЗоны диагностики:"
            for z in ctx.zones:
                prompt += (
                    f"\n- {z['label']}: {round(z['couple_avg'])}% "
                    f"({status_text.get(z['status'], z['status'])}, разрыв {round(z['gap'])}%)"
                )

        if ctx.bridge_analysis:
            ba = ctx.bridge_analysis
            prompt += f"\n\nМост понимания: {name_a} воспринимает — «{ba.get('partner_a_perspective', '')}»."
            prompt += f" {partner_name} воспринимает — «{ba.get('partner_b_perspective', '')}»."
            prompt += f" Общая почва: {ba.get('common_ground', '')}."

        if ctx.strengths:
            ss = ctx.strengths
            prompt += f"\n\nСильные стороны пары: {ss.get('headline', '')}."
            strengths = ss.get('strengths', [])
            if strengths:
                prompt += f" Конкретно: {', '.join(strengths[:3])}."

        if isinstance(ctx.problem_chain, list) and ctx.problem_chain:
            root = ctx.problem_chain[0]
            prompt += f"\n\nКорневая проблема по данным диагностики: {root.get('problem', '')}."

        if ctx.family_values:
            prompt += f"\n\nЦенности этой семьи: {', '.join(ctx.family_values[:3])}."
        if ctx.communication_rules:
            prompt += f" Их правила общения: {ctx.communication_rules[0]}."

        return prompt

    @classmethod
    def _build_greeting(cls, conversation: AIConversation, topic: str = None) -> str:
        from apps.ai.context_builder.builder import ContextBuilder

        user_name = conversation.user.first_name
        ctx       = ContextBuilder.build(conversation.couple)

        if ctx.weak_zones:
            zone_label = ctx.weak_zones[0]['label']
            return (
                f"Привет, {user_name}! Я вижу результаты вашей диагностики. "
                f"Хочу обратить внимание на зону «{zone_label}» — там есть важные моменты для работы. "
                f"С чего хотите начать?"
            )

        return (
            f"Привет, {user_name}! Я ваш AI-консультант по отношениям. "
            f"Я здесь, чтобы помочь вам лучше понять себя и партнёра. "
            f"О чём хотите поговорить?"
        )


class AIInsightService:
    @staticmethod
    def generate_insights(result) -> dict:
        import json
        try:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(result)
            couple = result.couple
            name_a = couple.partner_a.first_name
            name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            zone_summary = '\n'.join([
                f"- {z['label']}: {name_a} {round(z['partner_a']['percent'])}%, "
                f"{name_b} {round(z['partner_b']['percent'])}%, gap {round(z['gap'])}%"
                for z in zones
            ])

            messages = [
                {
                    'role': 'system',
                    'content': (
                        'You are a relationship analyst. '
                        'Return ONLY valid JSON without markdown.'
                    ),
                },
                {
                    'role': 'user',
                    'content': (
                        f"Give 3 short insights (1-2 sentences each) about the diagnostic results "
                        f"for the couple {name_a} and {name_b}:\n{zone_summary}\n\n"
                        f"Return in three languages with this exact structure:\n"
                        f'{{"ru": ["инсайт 1", "инсайт 2", "инсайт 3"], '
                        f'"en": ["insight 1", "insight 2", "insight 3"], '
                        f'"uz": ["tahlil 1", "tahlil 2", "tahlil 3"]}}'
                    ),
                },
            ]

            provider = AIProviderFactory.get()
            response_text = provider.complete(messages)
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                data = json.loads(response_text[start:end])
                if isinstance(data, dict) and 'ru' in data:
                    return data
        except Exception:
            logger.exception("Failed to parse AI zone analysis response as JSON")
        return {}
