"""
AI-генерация персонализированных практик для пары.

Вход:  Couple  →  ContextBuilder.build(couple)
Выход: DailyAssignment с 5 AI-сгенерированными слотами (is_ai_generated=True)

Схема слотов:
  main         — основная практика дня (Trust / Communication Exercise)
  conversation — тема для разговора    (Conversation Topic)
  gesture      — романтический жест    (Romantic Gesture)
  activity     — совместная активность (Shared Activity)
  growth       — вопрос дня            (Question of the Day)

При недоступности OpenAI — fallback на библиотечную генерацию.
"""

import json
import logging
from datetime import date, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

# Порядок слотов и их заголовки для промпта
SLOT_DESCRIPTIONS = {
    'main':         'Основная практика дня — упражнение на доверие / коммуникацию / близость (15–30 мин)',
    'conversation': 'Тема для разговора — глубокий вопрос или обсуждение для пары (10–20 мин)',
    'gesture':      'Романтический жест — маленькое, но значимое действие для партнёра (5–10 мин)',
    'activity':     'Совместная активность — что-то сделать вместе сегодня (20–60 мин)',
    'growth':       'Вопрос дня — саморефлексия или вопрос к партнёру (5 мин)',
}

VALID_CATEGORIES = frozenset({
    'communication', 'trust', 'intimacy', 'gratitude',
    'romance', 'finances', 'relatives', 'children',
})

# ── System prompt ─────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
Ты — AI-генератор персонализированных практик для пар приложения «Крепкая семья».

Генерируй 5 заданий на сегодня, строго соблюдая инструкции:

1. Учитывай слабые зоны отношений — делай акцент именно на них.
2. Учитывай уровень семьи: 1–3 = начинающие (простые задания), 4–7 = средний (умеренная глубина), 8–10 = опытные (сложные упражнения).
3. Каждое задание конкретно и выполнимо за один день без специального оборудования.
4. НЕ повторяй задания из списка недавних практик.
5. Тон: тёплый, поддерживающий, без давления и оценки.
6. Все тексты только на русском языке.
7. Возвращай ТОЛЬКО валидный JSON без комментариев, markdown-блоков или пояснений.

Типы заданий:
  main         — основная практика дня (Trust / Communication Exercise, 15–30 мин)
  conversation — тема для разговора (Conversation Topic, 10–20 мин)
  gesture      — романтический жест (Romantic Gesture, 5–10 мин)
  activity     — совместная активность (Shared Activity, 20–60 мин)
  growth       — вопрос дня (Question of the Day, 5 мин)

Допустимые категории: communication, trust, intimacy, gratitude, romance, finances, relatives, children

Структура ответа (строго этот JSON, ничего лишнего):
{
  "main":         {"title": "...", "description": "...", "instructions": "...", "category": "..."},
  "conversation": {"title": "...", "description": "...", "instructions": "...", "category": "..."},
  "gesture":      {"title": "...", "description": "...", "instructions": "...", "category": "..."},
  "activity":     {"title": "...", "description": "...", "instructions": "...", "category": "..."},
  "growth":       {"title": "...", "description": "...", "instructions": "...", "category": "..."}
}

Поля:
  title        — короткое название задания (3–8 слов)
  description  — зачем это задание и что оно даст (1–2 предложения)
  instructions — пошаговое описание как выполнить (2–4 предложения)
  category     — одна из допустимых категорий выше
"""


class PracticeGenerationService:
    """
    Генерирует AI-персонализированные практики для пары через GPT.

    Пример использования:
        service = PracticeGenerationService()
        assignment = service.generate_for_today(couple)
        # assignment.is_ai_generated == True
    """

    def generate_for_today(self, couple) -> Optional[object]:
        """
        Генерирует DailyAssignment с AI-практиками на сегодня.
        Если на сегодня уже есть задание — возвращает None (не перезаписывает).
        При ошибке OpenAI — fallback на библиотечную генерацию.
        """
        from .models import DailyAssignment

        today = date.today()

        # Не перезаписываем существующее задание
        if DailyAssignment.objects.filter(couple=couple, date=today).exists():
            logger.info(
                'PracticeGenerationService: задание на %s для пары %s уже существует — пропуск',
                today, couple.id,
            )
            return None

        from apps.ai.context_builder.builder import ContextBuilder
        ctx  = ContextBuilder.build(couple)
        plan = self._get_plan(couple)

        try:
            raw_data = self._call_ai(ctx, plan)
            if raw_data:
                return self._save(couple, raw_data, plan, is_ai=True)
            logger.warning('PracticeGenerationService: пустой ответ от AI, переходим к fallback')
        except (ValueError, RuntimeError) as e:
            logger.warning('PracticeGenerationService: OpenAI недоступен (%s), fallback', e)
        except Exception as e:
            logger.error('PracticeGenerationService: неожиданная ошибка (%s), fallback', e, exc_info=True)

        return self._library_fallback(couple, plan)

    # ── AI call ────────────────────────────────────────────────────────────────

    def _call_ai(self, ctx, plan) -> Optional[dict]:
        from apps.ai.providers.factory import AIProviderFactory

        provider    = AIProviderFactory.get()
        user_prompt = self._build_user_prompt(ctx, plan)

        messages = [
            {'role': 'system', 'content': _SYSTEM_PROMPT},
            {'role': 'user',   'content': user_prompt},
        ]

        raw = provider.generate(messages, temperature=0.8, max_tokens=1800)
        logger.debug('PracticeGenerationService raw response:\n%s', raw)

        return self._parse_and_validate(raw)

    def _build_user_prompt(self, ctx, plan) -> str:
        _GENDER = {'male': 'мужчина', 'female': 'женщина', 'other': 'другое'}
        _EDU = {
            'secondary': 'среднее', 'vocational': 'среднее специальное',
            'incomplete_higher': 'неполное высшее', 'higher': 'высшее',
            'postgraduate': 'учёная степень',
        }
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
        _CHILD_GENDER = {'male': 'мальчик', 'female': 'девочка'}

        def _partner_line(name, gender, age, occupation, education, conflict, support):
            parts = [name]
            if gender and gender != 'prefer_not_to_say':
                parts.append(_GENDER.get(gender, gender))
            if age:
                parts.append(f'{age} лет')
            if occupation:
                parts.append(occupation)
            if education:
                parts.append(_EDU.get(education, education))
            line = ', '.join(parts)
            if conflict or support:
                styles = []
                if conflict:
                    styles.append(f'конфликты — {_CONFLICT.get(conflict, conflict)}')
                if support:
                    styles.append(f'поддержка — {_SUPPORT.get(support, support)}')
                line += f' [{"; ".join(styles)}]'
            return line

        lines = ['Контекст пары:']

        # ── Партнёры ──────────────────────────────────────────────────────
        lines.append(
            '• Партнёр A: ' + _partner_line(
                ctx.partner_a_name, ctx.partner_a_gender, ctx.partner_a_age,
                ctx.partner_a_occupation, ctx.partner_a_education,
                ctx.partner_a_conflict_style, ctx.partner_a_support_style,
            )
        )
        if ctx.partner_b_name and ctx.partner_b_name != 'партнёр':
            lines.append(
                '• Партнёр B: ' + _partner_line(
                    ctx.partner_b_name, ctx.partner_b_gender, ctx.partner_b_age,
                    ctx.partner_b_occupation, ctx.partner_b_education,
                    ctx.partner_b_conflict_style, ctx.partner_b_support_style,
                )
            )

        # ── Отношения ─────────────────────────────────────────────────────
        rel_parts = []
        if ctx.relationship_status:
            rel_parts.append(_REL_STATUS.get(ctx.relationship_status, ctx.relationship_status))
        if ctx.relationship_years is not None:
            rel_parts.append(f'{ctx.relationship_years} лет вместе')
        if ctx.marriage_years is not None:
            rel_parts.append(f'в браке {ctx.marriage_years} лет')
        if rel_parts:
            lines.append(f'• Отношения: {", ".join(rel_parts)}')

        # ── Семейный контекст ─────────────────────────────────────────────
        if ctx.lives_with_parents:
            lines.append('• Живут с родителями или родственниками')
        if ctx.relatives_influence_level:
            lines.append(f'• Влияние родственников на пару: {ctx.relatives_influence_level}/5')
        if ctx.religious_traditions_importance:
            lines.append(f'• Значимость религиозных традиций: {ctx.religious_traditions_importance}/5')

        # ── Семейные ценности ─────────────────────────────────────────────
        if ctx.couple_family_values:
            values_ru = [_FV.get(s, s) for s in ctx.couple_family_values]
            lines.append(f'• Семейные ценности пары: {", ".join(values_ru)}')

        # ── Дети ──────────────────────────────────────────────────────────
        if ctx.children:
            child_parts = []
            for c in ctx.children:
                age_str = f'{c["age"]} лет' if c.get('age') is not None else 'возраст неизвестен'
                gender_str = _CHILD_GENDER.get(c.get('gender', ''), '')
                child_parts.append(f'{gender_str} {age_str}'.strip())
            lines.append(f'• Дети ({len(ctx.children)}): {", ".join(child_parts)}')

        # ── Диагностика ───────────────────────────────────────────────────
        _ZONE_LABEL = {
            'communication': 'Коммуникация', 'trust': 'Доверие',
            'intimacy': 'Близость', 'conflict': 'Конфликты',
            'values': 'Ценности', 'finance': 'Финансы',
            'relatives': 'Родственники', 'future': 'Будущее',
        }
        if ctx.relationship_index is not None:
            crisis_ru = {
                'critical': 'критический',
                'warning':  'требует внимания',
                'none':     'стабильный',
            }.get(ctx.crisis_level, ctx.crisis_level)
            index_line = f'• Индекс отношений: {ctx.relationship_index}/100 ({crisis_ru})'
            if ctx.relationship_delta is not None:
                sign = '+' if ctx.relationship_delta >= 0 else ''
                index_line += f' [{sign}{ctx.relationship_delta} с прошлой диагностики]'
            lines.append(index_line)

        lines.append(f'• Уровень семьи: {ctx.family_level}/10')

        if ctx.zones:
            lines.append('• Таблица зон (зона | средний% | gap между партнёрами | динамика):')
            for z in ctx.zones:
                key = z['zone']
                avg = round(z['couple_avg'])
                gap = round(z.get('gap', 0))
                dyn = ''
                if key in ctx.zone_deltas:
                    d = ctx.zone_deltas[key]
                    sign = '+' if d['delta'] >= 0 else ''
                    dyn = f" {d['prev']}%→{d['curr']}% ({sign}{d['delta']}%)"
                lines.append(f'  – {z["label"]}: {avg}% | gap {gap}%{dyn}')

        priority_zones = []
        if ctx.priority_zone:
            priority_zones.append(f'1. {_ZONE_LABEL.get(ctx.priority_zone, ctx.priority_zone)}')
        if ctx.secondary_zone:
            priority_zones.append(f'2. {_ZONE_LABEL.get(ctx.secondary_zone, ctx.secondary_zone)}')
        if ctx.tertiary_zone:
            priority_zones.append(f'3. {_ZONE_LABEL.get(ctx.tertiary_zone, ctx.tertiary_zone)}')
        if priority_zones:
            lines.append(f'• Приоритетные зоны: {", ".join(priority_zones)}')

        if ctx.strengths:
            headline = ctx.strengths.get('headline', '')
            if headline:
                lines.append(f'• Сильная сторона пары: {headline}')

        if ctx.completed_practices:
            lines.append(
                f'• Последние выполненные практики: {", ".join(ctx.completed_practices[:5])}'
            )

        # ── Избегать повторов ─────────────────────────────────────────────
        recent = self._get_recent_titles(plan.couple if plan else None)
        if recent:
            lines.append(
                '\nНЕ повторять следующие задания (уже были в последние 30 дней):\n'
                + '\n'.join(f'  – {t}' for t in list(recent)[:30])
            )

        lines.append('\nСгенерируй 5 заданий на сегодня согласно инструкции.')
        return '\n'.join(lines)

    # ── Parse & validate ──────────────────────────────────────────────────────

    def _parse_and_validate(self, raw: str) -> Optional[dict]:
        try:
            s = raw.find('{')
            e = raw.rfind('}') + 1
            if s < 0 or e <= s:
                logger.warning('PracticeGenerationService: JSON не найден в ответе')
                return None

            data = json.loads(raw[s:e])
        except json.JSONDecodeError as err:
            logger.warning('PracticeGenerationService: ошибка парсинга JSON — %s', err)
            return None

        required_slots = {'main', 'conversation', 'gesture', 'activity', 'growth'}
        required_fields = {'title', 'description', 'instructions', 'category'}

        for slot in required_slots:
            if slot not in data:
                logger.warning('PracticeGenerationService: отсутствует слот «%s»', slot)
                return None
            entry = data[slot]
            for field in required_fields:
                if not entry.get(field):
                    logger.warning(
                        'PracticeGenerationService: слот «%s» не содержит поле «%s»', slot, field,
                    )
                    return None
            # Нормализуем категорию — если GPT вернул невалидную, ставим дефолт
            if entry['category'] not in VALID_CATEGORIES:
                logger.warning(
                    'PracticeGenerationService: невалидная категория «%s» в слоте «%s», исправляем',
                    entry['category'], slot,
                )
                entry['category'] = _default_category_for_slot(slot)

        return data

    # ── Save ──────────────────────────────────────────────────────────────────

    def _save(self, couple, data: dict, plan, is_ai: bool) -> object:
        from .models import DailyAssignment, AssignmentSlot, Practice

        today      = date.today()
        categories = list({data[s]['category'] for s in data})

        assignment = DailyAssignment.objects.create(
            couple          = couple,
            date            = today,
            categories_used = categories,
            is_ai_generated = is_ai,
        )

        from .services import _auto_link_academy_article

        slot_order = ['main', 'conversation', 'gesture', 'activity', 'growth']
        slots_to_create = []
        for slot_type in slot_order:
            if slot_type not in data:
                continue
            entry    = data[slot_type]
            practice = Practice.objects.create(
                title            = entry['title'],
                description      = entry['description'],
                instructions     = entry.get('instructions', ''),
                category         = entry['category'],
                slot_type        = slot_type,
                difficulty       = _difficulty_for_slot(slot_type),
                duration_minutes = _duration_for_slot(slot_type),
                is_active        = True,
                tags             = ['ai_generated'],
            )
            if slot_type == 'growth':
                _auto_link_academy_article(practice)
            slots_to_create.append(
                AssignmentSlot(
                    assignment = assignment,
                    slot_type  = slot_type,
                    practice   = practice,
                    completed  = False,
                )
            )

        AssignmentSlot.objects.bulk_create(slots_to_create)

        logger.info(
            'PracticeGenerationService: создано AI-задание %s для пары %s (is_ai=%s)',
            assignment.id, couple.id, is_ai,
        )
        from .models import DailyAssignment as DA
        return DA.objects.prefetch_related('slots__practice', 'slots__practice__academy_article').get(pk=assignment.pk)

    # ── Fallback ──────────────────────────────────────────────────────────────

    def _library_fallback(self, couple, plan) -> object:
        """Fallback: библиотечная генерация через PracticeService."""
        from .models import DailyAssignment
        from .services import PracticeService

        today = date.today()
        assignment, _ = DailyAssignment.objects.get_or_create(
            couple = couple,
            date   = today,
            defaults={'is_ai_generated': False},
        )
        PracticeService._fill_assignment(couple, assignment, plan)
        logger.info(
            'PracticeGenerationService: fallback — библиотечная генерация для пары %s', couple.id,
        )
        return DailyAssignment.objects.prefetch_related('slots__practice', 'slots__practice__academy_article').get(pk=assignment.pk)

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _get_plan(couple):
        from .models import FamilyDevelopmentPlan
        plan, _ = FamilyDevelopmentPlan.objects.get_or_create(couple=couple)
        plan.couple = couple  # ensure reverse access in _build_user_prompt
        return plan

    @staticmethod
    def _get_recent_titles(couple) -> set:
        if not couple:
            return set()
        from .models import AssignmentSlot

        cutoff = date.today() - timedelta(days=30)
        return set(
            AssignmentSlot.objects
            .filter(
                assignment__couple    = couple,
                assignment__date__gte = cutoff,
                assignment__date__lt  = date.today(),
                practice__isnull      = False,
            )
            .values_list('practice__title', flat=True)
            .order_by('-assignment__date')[:30]
        )


# ── Module-level helpers ──────────────────────────────────────────────────────

def _default_category_for_slot(slot_type: str) -> str:
    return {
        'main':         'communication',
        'conversation': 'trust',
        'gesture':      'romance',
        'activity':     'intimacy',
        'growth':       'communication',
    }.get(slot_type, 'communication')


def _difficulty_for_slot(slot_type: str) -> str:
    return {
        'main':         'medium',
        'conversation': 'easy',
        'gesture':      'easy',
        'activity':     'medium',
        'growth':       'easy',
    }.get(slot_type, 'easy')


def _duration_for_slot(slot_type: str) -> int:
    return {
        'main':         20,
        'conversation': 15,
        'gesture':      5,
        'activity':     30,
        'growth':       5,
    }.get(slot_type, 10)
