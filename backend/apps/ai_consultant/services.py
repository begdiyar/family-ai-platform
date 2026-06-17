from typing import Generator
from apps.users.models import User
from apps.couples.models import Couple
from .models import AIConversation, AIMessage
from .repositories import AIConversationRepository, AIMessageRepository
from .providers import AIProviderFactory

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
        couple = conversation.couple
        name_a = couple.partner_a.first_name
        name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'
        user_name = conversation.user.first_name
        partner_name = name_b if user_name == name_a else name_a

        prompt = SYSTEM_PROMPT_BASE
        prompt += f"\n\nТы разговариваешь с {user_name}. Их партнёр — {partner_name}."

        # Диагностика
        from apps.analytics.repositories import AnalyticsRepository
        result = AnalyticsRepository.get_latest_for_couple(couple)
        if result:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(result)
            overall = round(result.overall_score)

            if result.crisis_level == 'critical':
                prompt += f"\n\n⚠️ ВАЖНО: Общий балл пары {overall}% — критический уровень. Будь особенно бережным и поддерживающим."
            elif result.crisis_level == 'warning':
                prompt += f"\n\nОбщий балл пары: {overall}% (требует внимания)."
            else:
                prompt += f"\n\nОбщий балл пары: {overall}%."

            if zones:
                status_text = {'strong': 'сильная', 'growth': 'зона роста', 'attention': 'требует внимания'}
                prompt += "\nЗоны диагностики:"
                for z in zones:
                    prompt += (
                        f"\n- {z['label']}: {round(z['couple_avg'])}% "
                        f"({status_text.get(z['status'], z['status'])}, разрыв {round(z['gap'])}%)"
                    )

            if result.bridge_analysis:
                ba = result.bridge_analysis
                prompt += f"\n\nМост понимания: {name_a} воспринимает — «{ba.get('partner_a_perspective', '')}»."
                prompt += f" {partner_name} воспринимает — «{ba.get('partner_b_perspective', '')}»."
                prompt += f" Общая почва: {ba.get('common_ground', '')}."

            if result.strengths_summary:
                ss = result.strengths_summary
                prompt += f"\n\nСильные стороны пары: {ss.get('headline', '')}."
                strengths = ss.get('strengths', [])
                if strengths:
                    prompt += f" Конкретно: {', '.join(strengths[:3])}."

            if result.problem_chain:
                root = result.problem_chain[0] if result.problem_chain else None
                if root:
                    prompt += f"\n\nКорневая проблема по данным диагностики: {root.get('problem', '')}."

        # Конституция
        try:
            from apps.constitution.models import FamilyConstitution
            constitution = FamilyConstitution.objects.filter(couple=couple).first()
            if constitution and any([constitution.values, constitution.communication_rules]):
                if constitution.values:
                    prompt += f"\n\nЦенности этой семьи: {', '.join(constitution.values[:3])}."
                if constitution.communication_rules:
                    prompt += f" Их правила общения: {constitution.communication_rules[0]}."
        except Exception:
            pass

        return prompt

    @classmethod
    def _build_greeting(cls, conversation: AIConversation, topic: str = None) -> str:
        user_name = conversation.user.first_name
        couple = conversation.couple

        from apps.analytics.repositories import AnalyticsRepository
        result = AnalyticsRepository.get_latest_for_couple(couple)

        if result:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(result)
            attention = [z for z in zones if z['status'] == 'attention']
            if attention:
                zone_label = attention[0]['label']
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
    def generate_insights(result) -> list:
        try:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(result)
            couple = result.couple
            name_a = couple.partner_a.first_name
            name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            zone_summary = '\n'.join([
                f"- {z['label']}: {name_a} {round(z['partner_a']['percent'])}%, "
                f"{name_b} {round(z['partner_b']['percent'])}%, расхождение {round(z['gap'])}%"
                for z in zones
            ])

            messages = [
                {'role': 'system', 'content': 'Ты — аналитик отношений. Отвечай кратко и по делу на русском языке.'},
                {'role': 'user', 'content': (
                    f"Дай 3 коротких инсайта (по 1-2 предложения каждый) по результатам диагностики пары "
                    f"{name_a} и {name_b}:\n{zone_summary}\n"
                    f"Формат: JSON массив строк."
                )},
            ]

            provider = AIProviderFactory.get()
            response_text = provider.complete(messages)
            import json
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            if start >= 0 and end > start:
                return json.loads(response_text[start:end])
        except Exception:
            pass
        return []
