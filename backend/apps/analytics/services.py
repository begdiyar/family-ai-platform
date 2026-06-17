import json
import logging
from decimal import Decimal

from apps.diagnostics.repositories import DiagnosticRepository, AnswerRepository
from apps.couples.models import Couple
from .models import AnalyticsResult
from .repositories import AnalyticsRepository

logger = logging.getLogger(__name__)

ZONES = ['communication', 'trust', 'intimacy', 'conflict', 'values', 'future']

ZONE_LABELS = {
    'communication': 'Коммуникация',
    'trust': 'Доверие',
    'intimacy': 'Близость',
    'conflict': 'Конфликты',
    'values': 'Ценности',
    'future': 'Будущее',
}

ZONE_WEIGHTS = {
    'communication': 1.2,
    'trust': 1.2,
    'intimacy': 1.0,
    'conflict': 1.1,
    'values': 0.9,
    'future': 0.8,
}


class AnalyticsService:
    @classmethod
    def calculate(cls, couple_id: str) -> AnalyticsResult:
        from django.db import transaction
        from apps.couples.repositories import CoupleRepository
        couple = CoupleRepository.get_by_id(couple_id)
        sessions = DiagnosticRepository.get_both_completed_sessions(couple)
        if not sessions or len(sessions) < 2:
            raise ValueError('Оба партнёра должны завершить диагностику')

        session_a = next(s for s in sessions if str(s.user_id) == str(couple.partner_a_id))
        session_b = next(s for s in sessions if str(s.user_id) == str(couple.partner_b_id))

        existing = AnalyticsResult.objects.filter(
            couple=couple, session_a=session_a, session_b=session_b
        ).first()
        if existing:
            return existing

        zone_scores_data = cls._calculate_zone_scores(session_a, session_b, couple)
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
    def _calculate_zone_scores(cls, session_a, session_b, couple) -> list:
        scores = []
        for zone in ZONES:
            answers_a = AnswerRepository.get_by_session_and_zone(session_a, zone)
            answers_b = AnswerRepository.get_by_session_and_zone(session_b, zone)
            score_a = cls._score_answers(answers_a)
            score_b = cls._score_answers(answers_b)
            max_score = Decimal('100.00')
            scores.append({'zone': zone, 'user_id': str(couple.partner_a_id), 'score': score_a, 'max_score': max_score})
            scores.append({'zone': zone, 'user_id': str(couple.partner_b_id), 'score': score_b, 'max_score': max_score})
        return scores

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
    def _generate_template_insights(zone_scores: list, couple) -> list:
        insights = []
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
        if gaps:
            top_zone, top_gap, _ = gaps[0]
            insights.append(
                f"Наибольшее расхождение — в зоне «{ZONE_LABELS[top_zone]}»: "
                f"разница составляет {round(top_gap)}%. Это важная точка для разговора."
            )

        best = max(zone_data.items(), key=lambda x: sum(x[1]) / len(x[1]))
        insights.append(
            f"Сильнейшая зона вашей пары — «{ZONE_LABELS[best[0]]}» "
            f"({round(sum(best[1]) / len(best[1]))}%). Опирайтесь на неё."
        )

        weak = min(zone_data.items(), key=lambda x: sum(x[1]) / len(x[1]))
        insights.append(
            f"Зона «{ZONE_LABELS[weak[0]]}» требует наибольшего внимания "
            f"({round(sum(weak[1]) / len(weak[1]))}%). Именно здесь сосредоточен ваш план."
        )
        return insights

    @classmethod
    def _generate_bridge_analysis(cls, zones: list, name_a: str, name_b: str, result) -> dict | None:
        try:
            from apps.ai_consultant.providers import AIProviderFactory

            zone_summary = '\n'.join([
                f"- {z['label']}: {name_a} {round(z['partner_a']['percent'])}%, "
                f"{name_b} {round(z['partner_b']['percent'])}%"
                for z in zones
            ])

            prompt = f"""Ты эксперт по семейным отношениям. Проанализируй результаты диагностики пары {name_a} и {name_b}.

Результаты по зонам:
{zone_summary}

Создай «Мост понимания» — анализ, который поможет супругам понять друг друга.
ВАЖНО: НЕ раскрывай личные ответы. Только обобщённый анализ.

Верни JSON строго такого формата:
{{
  "partner_a_perspective": "Что чувствует и в чём нуждается {name_a} (2-3 предложения, тепло и эмпатично)",
  "partner_b_perspective": "Что чувствует и в чём нуждается {name_b} (2-3 предложения, тепло и эмпатично)",
  "common_ground": "Что объединяет эту пару — их общие ценности и стремления (2 предложения)",
  "key_misunderstanding": "Главное недопонимание между ними, без обвинений (1-2 предложения)",
  "first_step": "Один конкретный первый шаг для улучшения отношений (1 предложение, действие)"
}}"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Отвечай только на русском языке. Возвращай только валидный JSON.'},
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

            prompt = f"""Создай раздел «Сильные стороны семьи» для пары {name_a} и {name_b}.

Лучшие зоны: {', '.join([f"{l} ({round(s)}%)" for l, s in all_avgs[:3]])}

Верни JSON:
{{
  "headline": "Краткая позитивная характеристика этой пары (1 предложение)",
  "strengths": ["Сила 1", "Сила 2", "Сила 3"],
  "achievement": "Конкретное достижение пары на основе их лучших зон (1 предложение)",
  "encouragement": "Мотивирующее послание этой паре (1-2 предложения)"
}}"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Отвечай только на русском языке. Только валидный JSON.'},
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

            prompt = f"""Построй карту проблем семьи на основе слабых зон: {weak_summary}.
Общий индекс: {round(overall)}%.

Создай цепочку из 4-6 связанных проблем, показывающую как одно ведёт к другому.

Верни JSON массив объектов:
[
  {{"step": 1, "problem": "Название проблемы", "description": "Краткое объяснение (1 предложение)"}},
  ...
]"""

            provider = AIProviderFactory.get()
            response = provider.complete([
                {'role': 'system', 'content': 'Отвечай только на русском языке. Только валидный JSON.'},
                {'role': 'user', 'content': prompt},
            ])
            start, end = response.find('['), response.rfind(']') + 1
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
