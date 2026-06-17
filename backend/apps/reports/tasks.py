from config.celery import app
import logging

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=2, default_retry_delay=30)
def generate_pdf_report(self, report_id: str):
    from .models import Report
    from .repositories import ReportRepository
    try:
        report = Report.objects.select_related('couple', 'result').get(id=report_id)
        from .pdf import PDFGenerator
        file_url = PDFGenerator.generate(report)
        ReportRepository.mark_ready(report, file_url)
        logger.info(f"PDF report {report_id} generated: {file_url}")
    except Exception as exc:
        logger.error(f"PDF generation failed for report {report_id}: {exc}")
        from .models import Report as R
        from .repositories import ReportRepository as RR
        try:
            r = R.objects.get(id=report_id)
            RR.mark_failed(r)
        except Exception:
            pass
        raise self.retry(exc=exc)


@app.task
def generate_monthly_reports():
    """Runs on the 1st of each month via Celery Beat."""
    from apps.couples.models import Couple
    from .models import Report
    from .repositories import ReportRepository

    active_couples = Couple.objects.filter(status='active').select_related('partner_a', 'partner_b')
    created_count = 0

    for couple in active_couples:
        try:
            report = Report.objects.create(
                couple=couple,
                created_by=couple.partner_a,
                report_type=Report.TYPE_MONTHLY,
                status=Report.STATUS_GENERATING,
            )
            generate_pdf_report.delay(str(report.id))
            created_count += 1
        except Exception as exc:
            logger.error(f"Failed to queue monthly report for couple {couple.id}: {exc}")

    logger.info(f"Monthly reports queued: {created_count}")
