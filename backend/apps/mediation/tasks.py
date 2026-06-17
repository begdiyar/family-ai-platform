from config.celery import app
import logging

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=2, default_retry_delay=30)
def analyze_conflict(self, session_id: str):
    try:
        from .models import ConflictSession
        from .services import MediationService
        session = ConflictSession.objects.select_related('couple__partner_a', 'couple__partner_b').get(id=session_id)
        MediationService.analyze(session)
        logger.info(f"Conflict analyzed for session {session_id}")
    except Exception as exc:
        logger.error(f"Conflict analysis task failed: {exc}")
        raise self.retry(exc=exc)
