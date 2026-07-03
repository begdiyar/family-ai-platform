import json
import logging

from apps.ai.providers.factory import AIProviderFactory

logger = logging.getLogger(__name__)


class AnalysisService:
    """AI-генерация аналитических выводов на основе данных диагностики."""

    def __init__(self):
        self.ai = AIProviderFactory.get()

    # ── Public API ────────────────────────────────────────────────────────

    def generate_insights(self, couple) -> list:
        """3 коротких инсайта по результатам диагностики пары."""
        try:
            from apps.analytics.repositories import AnalyticsRepository
            from apps.analytics.services import AnalyticsService

            result = AnalyticsRepository.get_latest_for_couple(couple)
            if not result:
                return []

            zones  = AnalyticsService.get_zone_detail_for_result(result)
            name_a = couple.partner_a.first_name
            name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            zone_summary = '\n'.join(
                f'- {z["label"]}: {name_a} {round(z["partner_a"]["percent"])}%, '
                f'{name_b} {round(z["partner_b"]["percent"])}%, '
                f'разрыв {round(z["gap"])}%'
                for z in zones
            )

            messages = [
                {
                    'role': 'system',
                    'content': (
                        'Ты аналитик семейных отношений. '
                        'Отвечай кратко и по делу только на русском языке. '
                        'Возвращай только валидный JSON-массив строк без пояснений.'
                    ),
                },
                {
                    'role': 'user',
                    'content': (
                        f'Дай 3 инсайта (1–2 предложения каждый) по диагностике '
                        f'пары {name_a} и {name_b}:\n{zone_summary}\n'
                        f'Общий балл: {round(float(result.overall_score))}%.'
                    ),
                },
            ]

            raw = self.ai.generate(messages, max_tokens=400)
            return self._parse_json_list(raw)

        except Exception as e:
            logger.error('AnalysisService.generate_insights failed: %s', e, exc_info=True)
            return []

    def generate_bridge_analysis(self, result) -> dict | None:
        """
        AI-мост понимания: перспективы партнёров, общая почва, первый шаг.
        Возвращает dict с ключами:
          partner_a_perspective, partner_b_perspective,
          common_ground, key_misunderstanding, first_step
        """
        try:
            from apps.analytics.services import AnalyticsService

            zones  = AnalyticsService.get_zone_detail_for_result(result)
            couple = result.couple
            name_a = couple.partner_a.first_name
            name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            zone_summary = '\n'.join(
                f'- {z["label"]}: {name_a} {round(z["partner_a"]["percent"])}%, '
                f'{name_b} {round(z["partner_b"]["percent"])}%'
                for z in zones
            )

            messages = [
                {
                    'role': 'system',
                    'content': (
                        'Ты психолог. Отвечай только на русском языке. '
                        'Возвращай только валидный JSON без пояснений.'
                    ),
                },
                {
                    'role': 'user',
                    'content': (
                        f'Диагностика пары {name_a} и {name_b}:\n{zone_summary}\n\n'
                        f'Верни JSON с полями:\n'
                        f'- partner_a_perspective: как видит ситуацию {name_a} (1 предложение)\n'
                        f'- partner_b_perspective: как видит ситуацию {name_b} (1 предложение)\n'
                        f'- common_ground: что объединяет пару (1 предложение)\n'
                        f'- key_misunderstanding: главное недопонимание (1 предложение)\n'
                        f'- first_step: конкретный первый шаг (1 предложение)'
                    ),
                },
            ]

            raw = self.ai.generate(messages, max_tokens=600)
            return self._parse_json_dict(raw)

        except Exception as e:
            logger.error('AnalysisService.generate_bridge_analysis failed: %s', e, exc_info=True)
            return None

    def generate_strengths_summary(self, result) -> dict | None:
        """
        AI-резюме сильных сторон пары.
        Возвращает dict: headline, strengths (list), achievement, encouragement
        """
        try:
            from apps.analytics.services import AnalyticsService

            zones   = AnalyticsService.get_zone_detail_for_result(result)
            strong  = [z for z in zones if z['status'] == 'strong']
            couple  = result.couple
            name_a  = couple.partner_a.first_name
            name_b  = couple.partner_b.first_name if couple.partner_b else 'партнёр'

            if not strong:
                return None

            labels = ', '.join(z['label'] for z in strong)
            messages = [
                {
                    'role': 'system',
                    'content': (
                        'Ты мотивационный коуч для пар. '
                        'Отвечай тепло и поддерживающе только на русском языке. '
                        'Возвращай только валидный JSON без пояснений.'
                    ),
                },
                {
                    'role': 'user',
                    'content': (
                        f'Сильные зоны пары {name_a} и {name_b}: {labels}.\n'
                        f'Общий балл: {round(float(result.overall_score))}%.\n\n'
                        f'Верни JSON с полями:\n'
                        f'- headline: заголовок об их силе (до 10 слов)\n'
                        f'- strengths: список из 3 конкретных сильных качеств (JSON массив строк)\n'
                        f'- achievement: что они уже достигли (1 предложение)\n'
                        f'- encouragement: вдохновляющее послание (1-2 предложения)'
                    ),
                },
            ]

            raw = self.ai.generate(messages, max_tokens=500)
            return self._parse_json_dict(raw)

        except Exception as e:
            logger.error('AnalysisService.generate_strengths_summary failed: %s', e, exc_info=True)
            return None

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_json_list(raw: str) -> list:
        try:
            s, e = raw.find('['), raw.rfind(']') + 1
            if s >= 0 and e > s:
                return json.loads(raw[s:e])
        except (json.JSONDecodeError, ValueError) as err:
            logger.warning('AnalysisService: failed to parse JSON list — %s', err)
        return []

    @staticmethod
    def _parse_json_dict(raw: str) -> dict | None:
        try:
            s, e = raw.find('{'), raw.rfind('}') + 1
            if s >= 0 and e > s:
                return json.loads(raw[s:e])
        except (json.JSONDecodeError, ValueError) as err:
            logger.warning('AnalysisService: failed to parse JSON dict — %s', err)
        return None
