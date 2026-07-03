import json
import logging
from decimal import Decimal

from apps.diagnostics.repositories import DiagnosticRepository, AnswerRepository
from apps.couples.models import Couple
from .models import AnalyticsResult
from .repositories import AnalyticsRepository

logger = logging.getLogger(__name__)

ZONES = ['communication', 'trust', 'intimacy', 'conflict', 'values', 'finance', 'relatives', 'future']

ZONE_LABELS = {
    'communication': 'Коммуникация',
    'trust': 'Доверие',
    'intimacy': 'Близость',
    'conflict': 'Конфликты',
    'values': 'Ценности',
    'finance': 'Финансы',
    'relatives': 'Родственники',
    'future': 'Будущее',
}

ZONE_LABELS_I18N = {
    'communication': {'ru': 'Коммуникация', 'en': 'Communication', 'uz': 'Muloqot'},
    'trust':         {'ru': 'Доверие',       'en': 'Trust',          'uz': 'Ishonch'},
    'intimacy':      {'ru': 'Близость',       'en': 'Intimacy',       'uz': 'Yaqinlik'},
    'conflict':      {'ru': 'Конфликты',      'en': 'Conflict',       'uz': 'Mojarolar'},
    'values':        {'ru': 'Ценности',       'en': 'Values',         'uz': 'Qadriyatlar'},
    'finance':       {'ru': 'Финансы',        'en': 'Finance',        'uz': 'Moliya'},
    'relatives':     {'ru': 'Родственники',   'en': 'Relatives',      'uz': 'Qarindoshlar'},
    'future':        {'ru': 'Будущее',        'en': 'Future',         'uz': 'Kelajak'},
}

ZONE_WEIGHTS = {
    'communication': 1.2,
    'trust': 1.2,
    'intimacy': 1.0,
    'conflict': 1.1,
    'values': 0.9,
    'finance': 1.0,
    'relatives': 0.9,
    'future': 0.8,
}


class AnalyticsService:
    @classmethod
    def calculate(cls, couple_id: str) -> AnalyticsResult:
        from django.db import transaction
        from apps.couples.repositories import CoupleRepository
        from apps.diagnostics.models import DiagnosticSession as DS
        couple = CoupleRepository.get_by_id(couple_id)

        # Собираем ВСЕ завершённые сессии обоих партнёров (кумулятивно по уровням)
        sessions_a = list(DS.objects.filter(
            couple=couple,
            user=couple.partner_a,
            status=DS.STATUS_COMPLETED,
        ))
        sessions_b = list(DS.objects.filter(
            couple=couple,
            user=couple.partner_b,
            status=DS.STATUS_COMPLETED,
        )) if couple.partner_b else []

        if not sessions_a or not sessions_b:
            raise ValueError('Оба партнёра должны завершить диагностику')

        # Для FK берём последние сессии
        session_a = max(sessions_a, key=lambda s: s.finished_at or s.started_at)
        session_b = max(sessions_b, key=lambda s: s.finished_at or s.started_at)

        # Не создавать дубликат, если результат для этой пары сессий уже существует
        existing = AnalyticsResult.objects.filter(
            couple=couple, session_a=session_a, session_b=session_b
        ).first()
        if existing:
            return existing

        zone_scores_data = cls._calculate_zone_scores_multi(sessions_a, sessions_b, couple)
        if not zone_scores_data:
            raise ValueError('Нет данных для расчёта — ни одна зона не покрыта')

        overall = cls._calculate_overall(zone_scores_data)
        crisis_level = cls._determine_crisis_level(float(overall))
        insights = cls._generate_template_insights(zone_scores_data, couple)

        with transaction.atomic():
            result = AnalyticsRepository.create(
                couple=couple,
                session_a=session_a,
                session_b=session_b,
                overall_score=overall,
                key_insights=insights,
            )
            result.crisis_level = crisis_level
            result.save(update_fields=['crisis_level'])
            AnalyticsRepository.bulk_create_zone_scores(result, zone_scores_data)

        # Update family development plan with new zone priorities
        try:
            from apps.practices.services import PracticeService
            PracticeService.update_plan_from_analytics(couple, result)
        except Exception:
            logger.warning('Could not update FamilyDevelopmentPlan after analytics calculation')

        # Unlock next diagnostic level if XP gate is satisfied
        try:
            from apps.diagnostics.services import JourneyService
            JourneyService.check_and_unlock_next_level(couple)
        except Exception:
            logger.warning('Could not check level unlock after analytics for couple %s', couple.id)

        return result

    @classmethod
    def enrich_with_ai(cls, result: AnalyticsResult) -> None:
        """Вызывается из Celery после base-расчёта. Добавляет AI-анализ."""
        try:
            zones = cls.get_zone_detail_for_result(result)
            couple = result.couple
            name_a = couple.partner_a.first_name
            name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            bridge = cls._generate_bridge_analysis(zones, name_a, name_b, result)
            strengths = cls._generate_strengths_summary(zones, name_a, name_b)
            problem_chain = cls._generate_problem_chain(zones, float(result.overall_score))

            update_fields = []
            if bridge:
                result.bridge_analysis = bridge
                update_fields.append('bridge_analysis')
            if strengths:
                result.strengths_summary = strengths
                update_fields.append('strengths_summary')
            if problem_chain:
                result.problem_chain = problem_chain
                update_fields.append('problem_chain')

            if update_fields:
                result.save(update_fields=update_fields)
        except Exception as e:
            logger.warning(f"AI enrichment failed for result {result.id}: {e}")

    @classmethod
    def _calculate_zone_scores_multi(cls, sessions_a: list, sessions_b: list, couple) -> list:
        """Кумулятивный расчёт по всем сессиям (поддерживает многоуровневую диагностику)."""
        from apps.diagnostics.repositories import AnswerRepository as AR
        scores = []
        max_score = Decimal('100.00')
        for zone in ZONES:
            answers_a = AR.get_by_sessions_and_zone(sessions_a, zone)
            answers_b = AR.get_by_sessions_and_zone(sessions_b, zone)
            if not answers_a or not answers_b:
                continue  # зона ещё не пройдена
            score_a = cls._score_answers(answers_a)
            score_b = cls._score_answers(answers_b)
            scores.append({'zone': zone, 'user_id': str(couple.partner_a_id), 'score': score_a, 'max_score': max_score})
            scores.append({'zone': zone, 'user_id': str(couple.partner_b_id), 'score': score_b, 'max_score': max_score})
        return scores

    @classmethod
    def _calculate_zone_scores(cls, session_a, session_b, couple) -> list:
        """Обратная совместимость — оборачивает в multi."""
        return cls._calculate_zone_scores_multi([session_a], [session_b], couple)

    @staticmethod
    def _score_answers(answers) -> Decimal:
        scale_values = [a.value_scale for a in answers if a.value_scale is not None]
        if not scale_values:
            return Decimal('0.00')
        avg = sum(scale_values) / (len(scale_values) * 5)
        return Decimal(str(round(avg * 100, 2)))

    @classmethod
    def _calculate_overall(cls, zone_scores: list) -> Decimal:
        if not zone_scores:
            return Decimal('0.00')
        total_weighted = Decimal('0')
        total_weight = Decimal('0')
        processed_zones = set()
        for item in zone_scores:
            zone = item['zone']
            if zone in processed_zones:
                continue
            zone_items = [s for s in zone_scores if s['zone'] == zone]
            zone_avg = sum(s['score'] for s in zone_items) / len(zone_items)
            weight = Decimal(str(ZONE_WEIGHTS.get(zone, 1.0)))
            total_weighted += zone_avg * weight
            total_weight += weight
            processed_zones.add(zone)
        return Decimal(str(round(total_weighted / total_weight, 2))) if total_weight else Decimal('0')

    @staticmethod
    def _determine_crisis_level(overall: float) -> str:
        if overall < 35:
            return AnalyticsResult.CRISIS_CRITICAL
        if overall < 50:
            return AnalyticsResult.CRISIS_WARNING
        return AnalyticsResult.CRISIS_NONE

    @staticmethod
    def _generate_template_insights(zone_scores: list, couple) -> dict:
        zone_data = {}
        for item in zone_scores:
            z = item['zone']
            if z not in zone_data:
                zone_data[z] = []
            zone_data[z].append(float(item['score']))

        gaps = []
        for zone, scores in zone_data.items():
            if len(scores) == 2:
                gap = abs(scores[0] - scores[1])
                gaps.append((zone, gap, scores))
        gaps.sort(key=lambda x: x[1], reverse=True)

        best = max(zone_data.items(), key=lambda x: sum(x[1]) / len(x[1]))
        weak = min(zone_data.items(), key=lambda x: sum(x[1]) / len(x[1]))

        result = {'ru': [], 'en': [], 'uz': []}
        for lang in ('ru', 'en', 'uz'):
            lbl = ZONE_LABELS_I18N
            items = []
            if gaps:
                top_zone, top_gap, _ = gaps[0]
                lbl_top = lbl[top_zone][lang]
                if lang == 'ru':
                    items.append(f"Наибольшее расхождение — в зоне «{lbl_top}»: разница составляет {round(top_gap)}%. Это важная точка для разговора.")
                elif lang == 'en':
                    items.append(f"The biggest gap is in the \"{lbl_top}\" zone: {round(top_gap)}% difference. This is an important point for conversation.")
                else:
                    items.append(f"Eng katta farq «{lbl_top}» zonasida: {round(top_gap)}% farq. Bu muhokama uchun muhim nuqta.")

            best_zone, best_scores = best
            best_score = round(sum(best_scores) / len(best_scores))
            lbl_best = lbl[best_zone][lang]
            if lang == 'ru':
                items.append(f"Сильнейшая зона вашей пары — «{lbl_best}» ({best_score}%). Опирайтесь на неё.")
            elif lang == 'en':
                items.append(f"Your couple's strongest zone is \"{lbl_best}\" ({best_score}%). Build on this strength.")
            else:
                items.append(f"Juftligingizdagi eng kuchli zona — «{lbl_best}» ({best_score}%). Shu kuchingizga tayaning.")

            weak_zone, weak_scores = weak
            weak_score = round(sum(weak_scores) / len(weak_scores))
            lbl_weak = lbl[weak_zone][lang]
            if lang == 'ru':
                items.append(f"Зона «{lbl_weak}» требует наибольшего внимания ({weak_score}%). Именно здесь сосредоточен ваш план.")
            elif lang == 'en':
                items.append(f"The \"{lbl_weak}\" zone needs the most attention ({weak_score}%). This is where your plan should focus.")
            else:
                items.append(f"«{lbl_weak}» zonasi eng ko'p e'tiborni talab qiladi ({weak_score}%). Rejangiz aynan shu yerga qaratilishi kerak.")

            result[lang] = items
        return result

    @classmethod
    def _generate_bridge_analysis(cls, zones: list, name_a: str, name_b: str, result) -> dict | None:
        try:
            from apps.ai_consultant.providers import AIProviderFactory

            zone_summary = '\n'.join([
                f"- {z['label']}: {name_a} {round(z['partner_a']['percent'])}%, "
                f"{name_b} {round(z['partner_b']['percent'])}%"
                for z in zones
            ])

            prompt = f"""You are a family psychology expert. Analyse the diagnostic results for the couple {name_a} and {name_b}.

Zone results:
{zone_summary}

Create a "Bridge of Understanding" analysis that helps the partners understand each other.
IMPORTANT: Do NOT reveal individual answers. Only generalised analysis.

Return ONLY valid JSON with this exact structure — text in three languages (ru=Russian, en=English, uz=Uzbek):
{{
  "ru": {{
    "partner_a_perspective": "Что чувствует и в чём нуждается {name_a} (2-3 предложения)",
    "partner_b_perspective": "Что чувствует и в чём нуждается {name_b} (2-3 предложения)",
    "common_ground": "Что объединяет эту пару (2 предложения)",
    "key_misunderstanding": "Главное недопонимание, без обвинений (1-2 предложения)",
    "first_step": "Один конкретный первый шаг (1 предложение)"
  }},
  "en": {{
    "partner_a_perspective": "What {name_a} feels and needs (2-3 sentences)",
    "partner_b_perspective": "What {name_b} feels and needs (2-3 sentences)",
    "common_ground": "What unites this couple (2 sentences)",
    "key_misunderstanding": "The main misunderstanding, no blame (1-2 sentences)",
    "first_step": "One concrete first step (1 sentence)"
  }},
  "uz": {{
    "partner_a_perspective": "{name_a} nima his qiladi va nimaga muhtoj (2-3 gap)",
    "partner_b_perspective": "{name_b} nima his qiladi va nimaga muhtoj (2-3 gap)",
    "common_ground": "Bu juftlikni birlashtiruvchi narsa (2 gap)",
    "key_misunderstanding": "Asosiy tushunmovchilik, aybsiz (1-2 gap)",
    "first_step": "Bitta aniq birinchi qadam (1 gap)"
  }}
}}"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Return ONLY valid JSON without markdown.'},
                {'role': 'user', 'content': prompt},
            ])
            start, end = response.find('{'), response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception as e:
            logger.warning(f"Bridge analysis generation failed: {e}")
        return None

    @classmethod
    def _generate_strengths_summary(cls, zones: list, name_a: str, name_b: str) -> dict | None:
        try:
            from apps.ai_consultant.providers import AIProviderFactory

            strong_zones = [z for z in zones if z['status'] == 'strong']
            all_avgs = [(z['label'], z['couple_avg']) for z in zones]
            all_avgs.sort(key=lambda x: x[1], reverse=True)

            prompt = f"""You are a family psychology expert. Create a "Family Strengths" section for the couple {name_a} and {name_b}.

Top zones: {', '.join([f"{l} ({round(s)}%)" for l, s in all_avgs[:3]])}

Return ONLY valid JSON with this exact structure — text in three languages:
{{
  "ru": {{
    "headline": "Краткая позитивная характеристика этой пары (1 предложение)",
    "strengths": ["Сила 1", "Сила 2", "Сила 3"],
    "achievement": "Конкретное достижение пары (1 предложение)",
    "encouragement": "Мотивирующее послание (1-2 предложения)"
  }},
  "en": {{
    "headline": "Brief positive description of this couple (1 sentence)",
    "strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "achievement": "Specific couple achievement (1 sentence)",
    "encouragement": "Motivating message (1-2 sentences)"
  }},
  "uz": {{
    "headline": "Juftlik haqida qisqa ijobiy tavsif (1 gap)",
    "strengths": ["Kuch 1", "Kuch 2", "Kuch 3"],
    "achievement": "Juftlikning aniq yutug'i (1 gap)",
    "encouragement": "Rag'batlantiruvchi xabar (1-2 gap)"
  }}
}}"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Return ONLY valid JSON without markdown.'},
                {'role': 'user', 'content': prompt},
            ])
            start, end = response.find('{'), response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception as e:
            logger.warning(f"Strengths generation failed: {e}")
        return None

    @classmethod
    def _generate_problem_chain(cls, zones: list, overall: float) -> list | None:
        try:
            from apps.ai_consultant.providers import AIProviderFactory

            weak_zones = [z for z in zones if z['status'] in ('attention', 'growth')]
            if not weak_zones:
                return None

            weak_summary = ', '.join([f"{z['label']} ({round(z['couple_avg'])}%)" for z in weak_zones[:3]])

            prompt = f"""You are a family psychology expert. Build a problem chain for the couple based on weak zones: {weak_summary}.
Overall index: {round(overall)}%.

Create a chain of 4-6 connected problems showing how one leads to another.

Return ONLY valid JSON with this exact structure — text in three languages:
{{
  "ru": [
    {{"step": 1, "problem": "Название проблемы", "description": "Краткое объяснение (1 предложение)"}},
    ...
  ],
  "en": [
    {{"step": 1, "problem": "Problem name", "description": "Brief explanation (1 sentence)"}},
    ...
  ],
  "uz": [
    {{"step": 1, "problem": "Muammo nomi", "description": "Qisqa izoh (1 gap)"}},
    ...
  ]
}}"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Return ONLY valid JSON without markdown.'},
                {'role': 'user', 'content': prompt},
            ])
            start, end = response.find('{'), response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception as e:
            logger.warning(f"Problem chain generation failed: {e}")
        return None

    @classmethod
    def get_zone_detail_for_result(cls, result: AnalyticsResult) -> list:
        zones_out = []
        zone_scores = result.zone_scores.select_related('user').all()
        for zone in ZONES:
            zone_items = [zs for zs in zone_scores if zs.zone == zone]
            if len(zone_items) < 2:
                continue
            a_score = next((zs for zs in zone_items if str(zs.user_id) == str(result.session_a.user_id)), None)
            b_score = next((zs for zs in zone_items if str(zs.user_id) == str(result.session_b.user_id)), None)
            if not a_score or not b_score:
                continue
            gap = abs(a_score.percent - b_score.percent)
            avg = (a_score.percent + b_score.percent) / 2
            status = 'strong' if avg >= 70 else ('attention' if avg < 50 else 'growth')
            zones_out.append({
                'zone': zone,
                'label': ZONE_LABELS[zone],
                'partner_a': {'score': float(a_score.score), 'percent': a_score.percent},
                'partner_b': {'score': float(b_score.score), 'percent': b_score.percent},
                'couple_avg': avg,
                'gap': gap,
                'status': status,
            })
        return zones_out


class AnalyticsInsightService:
    """Generates and caches the AI Insight Report for an AnalyticsResult."""

    _ZONE_LABEL = {
        'communication': 'Коммуникация', 'trust': 'Доверие',
        'intimacy': 'Близость', 'conflict': 'Конфликты',
        'values': 'Ценности', 'finance': 'Финансы',
        'relatives': 'Родственники', 'future': 'Будущее',
    }
    _FV = {
        'respect': 'уважение', 'trust': 'доверие', 'love': 'любовь',
        'children': 'дети', 'education': 'образование',
        'financial_stability': 'финансовая стабильность', 'career': 'карьера',
        'faith': 'вера', 'traditions': 'традиции', 'travel': 'путешествия',
        'self_development': 'саморазвитие', 'health': 'здоровье',
    }
    _CRISIS = {
        'critical': 'критический',
        'warning': 'требует внимания',
        'none': 'стабильный',
    }

    @classmethod
    def generate(cls, result: AnalyticsResult):
        """Generate insight if not already present. Idempotent."""
        from .models import AnalyticsInsight
        logger.info("INSIGHT-GEN-1: generate() entered for result %s", result.id)
        existing = AnalyticsInsight.objects.filter(analytics_result=result).first()
        if existing:
            logger.info("INSIGHT-GEN-1a: existing insight found id=%s, returning early", existing.id)
            return existing
        try:
            logger.info("INSIGHT-GEN-2: calling _call_ai()")
            data = cls._call_ai(result)
            logger.info("INSIGHT-GEN-3: _call_ai returned type=%s", type(data).__name__ if data is not None else 'None')
            if not data:
                logger.warning("INSIGHT-GEN-3a: _call_ai returned None — no AnalyticsInsight will be created")
                return None
            logger.info("INSIGHT-GEN-4: creating AnalyticsInsight with keys=%s", list(data.keys()))
            # data = {"ru": {field: val, ...}, "en": {...}, "uz": {...}}
            # Store each field as {"ru": "...", "en": "...", "uz": "..."} for language-aware serving
            text_fields = ['strengths_summary', 'growth_summary', 'attention_summary', 'ai_analysis', 'recommendation', 'next_focus']
            field_values = {
                field: {lang: data.get(lang, {}).get(field, '') for lang in ('ru', 'en', 'uz')}
                for field in text_fields
            }
            insight = AnalyticsInsight.objects.create(
                analytics_result=result,
                **field_values,
            )
            logger.info("INSIGHT-GEN-5: AnalyticsInsight created successfully id=%s", insight.id)
            return insight
        except Exception as e:
            logger.warning('AnalyticsInsightService.generate failed: %s', e, exc_info=True)
            return None

    @classmethod
    def _call_ai(cls, result: AnalyticsResult) -> dict | None:
        from apps.ai_consultant.providers import AIProviderFactory
        from apps.ai.context_builder.builder import ContextBuilder

        logger.info("INSIGHT-AI-1: _call_ai started for result %s", result.id)
        ctx = ContextBuilder.build(result.couple)
        zones = AnalyticsService.get_zone_detail_for_result(result)
        prompt = cls._build_prompt(ctx, zones)
        logger.info("INSIGHT-AI-2: prompt built (%d chars), getting provider", len(prompt))

        provider = AIProviderFactory.get()
        logger.info("INSIGHT-AI-3: provider=%s, calling complete()", type(provider).__name__)
        response = provider.complete([
            {
                'role': 'system',
                'content': (
                    'You are a family psychology expert. '
                    'Return ONLY valid JSON without markdown. '
                    'Generate all text in three languages simultaneously: ru (Russian), en (English), uz (Uzbek).'
                ),
            },
            {'role': 'user', 'content': prompt},
        ])
        logger.info("INSIGHT-AI-4: AI response received, length=%d", len(response) if response else 0)
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            data = json.loads(response[start:end])
            logger.info("INSIGHT-AI-5: JSON parsed ok, keys=%s", list(data.keys()))
            return data
        logger.warning("INSIGHT-AI-5a: no JSON object found in response: %.200s", response or '')
        return None

    @classmethod
    def _build_prompt(cls, ctx, zones: list) -> str:
        lines = [
            f'Пара: {ctx.partner_a_name} и {ctx.partner_b_name}',
            f'Индекс отношений: {ctx.relationship_index}/100 ({cls._CRISIS.get(ctx.crisis_level, ctx.crisis_level)})',
        ]

        if ctx.relationship_delta is not None:
            sign = '+' if ctx.relationship_delta >= 0 else ''
            lines.append(f'Динамика индекса: {sign}{ctx.relationship_delta} с прошлой диагностики')

        lines.append(f'Уровень семьи: {ctx.family_level}/10')

        if ctx.relationship_years is not None:
            lines.append(f'Стаж отношений: {ctx.relationship_years} лет')

        if ctx.children:
            lines.append(f'Детей: {len(ctx.children)}')

        # Zone table — AI-internal (gap never exposed to users)
        if zones:
            lines.append('')
            lines.append('Данные по зонам (только для AI, пользователю не показывать):')
            for z in zones:
                key = z['zone']
                avg = round(z['couple_avg'])
                gap = round(z.get('gap', 0))
                dyn = ''
                if key in ctx.zone_deltas:
                    d = ctx.zone_deltas[key]
                    sign = '+' if d['delta'] >= 0 else ''
                    dyn = f'  динамика {d["prev"]}%→{d["curr"]}% ({sign}{d["delta"]}%)'
                lines.append(f'  {z["label"]}: {avg}%, разрыв партнёров: {gap}%{dyn}')

        priority = []
        if ctx.priority_zone:
            priority.append(cls._ZONE_LABEL.get(ctx.priority_zone, ctx.priority_zone))
        if ctx.secondary_zone:
            priority.append(cls._ZONE_LABEL.get(ctx.secondary_zone, ctx.secondary_zone))
        if ctx.tertiary_zone:
            priority.append(cls._ZONE_LABEL.get(ctx.tertiary_zone, ctx.tertiary_zone))
        if priority:
            lines.append(f'Приоритет развития: {" → ".join(priority)}')

        if ctx.couple_family_values:
            vals = [cls._FV.get(s, s) for s in ctx.couple_family_values]
            lines.append(f'Семейные ценности: {", ".join(vals)}')

        lines.append('')
        lines.append(
            'Generate a personalised AI report in JSON. Be warm, non-judgmental. '
            'Do not mention numeric scores or the gap between partners.\n'
            'Return text in three languages (ru, en, uz) with this exact structure:\n'
            '{\n'
            '  "ru": {\n'
            '    "strengths_summary": "Краткое описание сильных сторон семьи (1-2 предложения)",\n'
            '    "growth_summary": "Какие зоны сейчас активно развиваются (1 предложение)",\n'
            '    "attention_summary": "Что требует внимания (1 предложение)",\n'
            '    "ai_analysis": "Основной анализ — что происходит в семье (2-3 предложения)",\n'
            '    "recommendation": "Практическая рекомендация на ближайшие 2 недели (1-2 предложения)",\n'
            '    "next_focus": "Почему именно эта зона выбрана следующей (1 предложение)"\n'
            '  },\n'
            '  "en": {\n'
            '    "strengths_summary": "Brief description of the family strengths (1-2 sentences)",\n'
            '    "growth_summary": "Which zones are actively developing now (1 sentence)",\n'
            '    "attention_summary": "What requires attention (1 sentence)",\n'
            '    "ai_analysis": "Main analysis — what is happening in the family (2-3 sentences)",\n'
            '    "recommendation": "Practical recommendation for the next 2 weeks (1-2 sentences)",\n'
            '    "next_focus": "Why this zone was chosen as the next focus (1 sentence)"\n'
            '  },\n'
            '  "uz": {\n'
            '    "strengths_summary": "Oilaning kuchli tomonlari haqida qisqa tavsif (1-2 gap)",\n'
            '    "growth_summary": "Qaysi sohalar hozir faol rivojlanmoqda (1 gap)",\n'
            '    "attention_summary": "Nima e\'tibor talab qiladi (1 gap)",\n'
            '    "ai_analysis": "Asosiy tahlil — oilada nima bo\'layapti (2-3 gap)",\n'
            '    "recommendation": "Keyingi 2 hafta uchun amaliy tavsiya (1-2 gap)",\n'
            '    "next_focus": "Nega aynan bu soha keyingi bosqich sifatida tanlandi (1 gap)"\n'
            '  }\n'
            '}'
        )

        return '\n'.join(lines)
