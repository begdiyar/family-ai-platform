from config.celery import app
import logging

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def calculate_analytics(self, couple_id: str):
    try:
        logger.info("INSIGHT-1: calculate_analytics started for couple %s", couple_id)
        from .services import AnalyticsService
        result = AnalyticsService.calculate(couple_id)
        logger.info("INSIGHT-2: AnalyticsService.calculate() returned result %s", result.id)
        generate_ai_insights.delay(str(result.id))
        logger.info("INSIGHT-3: generate_ai_insights.delay() called")
        generate_analytics_insight.delay(str(result.id))
        logger.info("INSIGHT-4: generate_analytics_insight.delay() called")
        logger.info(f"Analytics calculated for couple {couple_id}, result {result.id}")

        # AI-обогащение: мост понимания, сильные стороны, карта проблем
        try:
            from .services import AnalyticsService
            AnalyticsService.enrich_with_ai(result)
            logger.info(f"AI enrichment done for result {result.id}")
        except Exception as enrich_exc:
            logger.warning(f"AI enrichment failed: {enrich_exc}")

        # Автоматически создаём план сразу после аналитики
        try:
            from apps.plans.services import PlanService
            from shared.exceptions import BusinessLogicError
            couple = result.couple
            PlanService.create_plan(couple.partner_a, result_id=str(result.id))
            logger.info(f"Plan auto-created for couple {couple_id}")
        except BusinessLogicError as e:
            logger.info(f"Plan not auto-created ({e.code}): normal")
        except Exception as plan_exc:
            logger.warning(f"Plan auto-creation failed: {plan_exc}")

        return str(result.id)
    except Exception as exc:
        logger.error(f"Analytics calculation failed for couple {couple_id}: {exc}")
        raise self.retry(exc=exc)


@app.task(bind=True, max_retries=2, default_retry_delay=60)
def generate_analytics_insight(self, result_id: str):
    logger.info("INSIGHT-5: generate_analytics_insight task started for result %s", result_id)
    try:
        from .repositories import AnalyticsRepository
        from .services import AnalyticsInsightService
        result = AnalyticsRepository.get_by_id(result_id)
        if not result:
            logger.warning("INSIGHT-6a: result NOT FOUND for id %s", result_id)
            return
        logger.info("INSIGHT-6: result fetched ok, calling generate()")
        AnalyticsInsightService.generate(result)
        logger.info("INSIGHT-7: generate() returned — done for result %s", result_id)
    except Exception as exc:
        logger.error(f'Analytics insight generation failed for result {result_id}: {exc}')
        raise self.retry(exc=exc)


@app.task(bind=True, max_retries=2, default_retry_delay=30)
def generate_ai_insights(self, result_id: str):
    try:
        from .repositories import AnalyticsRepository
        from apps.ai_consultant.services import AIInsightService
        result = AnalyticsRepository.get_by_id(result_id)
        if not result:
            return
        insights = AIInsightService.generate_insights(result)
        if insights:
            AnalyticsRepository.update_insights(result, insights)
        logger.info(f"AI insights generated for result {result_id}")
    except Exception as exc:
        logger.error(f"AI insights generation failed for result {result_id}: {exc}")
        raise self.retry(exc=exc)
