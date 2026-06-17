import io
import boto3
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML


class PDFGenerator:
    @staticmethod
    def generate(report) -> str:
        if report.report_type == 'diagnostic':
            html_content = PDFGenerator._render_diagnostic(report)
        elif report.report_type == 'monthly':
            html_content = PDFGenerator._render_monthly(report)
        else:
            html_content = PDFGenerator._render_progress(report)

        pdf_bytes = HTML(string=html_content).write_pdf()
        file_key = f"reports/{report.couple_id}/{report.id}.pdf"
        PDFGenerator._upload_to_s3(pdf_bytes, file_key)

        public_base = settings.AWS_S3_PUBLIC_URL or settings.AWS_S3_ENDPOINT_URL
        if public_base:
            return f"{public_base}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_key}"
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"

    @staticmethod
    def _render_diagnostic(report) -> str:
        from apps.analytics.services import AnalyticsService
        context = {
            'report': report,
            'couple': report.couple,
            'result': report.result,
        }
        if report.result:
            context['zones'] = AnalyticsService.get_zone_detail_for_result(report.result)
        return render_to_string('reports/diagnostic.html', context)

    @staticmethod
    def _render_progress(report) -> str:
        context = {'report': report, 'couple': report.couple}
        return render_to_string('reports/progress.html', context)

    @staticmethod
    def _render_monthly(report) -> str:
        from django.utils import timezone
        from datetime import timedelta
        from apps.analytics.models import AnalyticsResult
        from apps.practices.models import PracticeCompletion
        from apps.mediation.models import ConflictSession
        from apps.plans.models import PlanTask, TaskCompletion

        couple = report.couple
        now = timezone.now()
        month_ago = now - timedelta(days=30)

        results = AnalyticsResult.objects.filter(
            couple=couple, created_at__gte=month_ago
        ).order_by('created_at')

        first_result = results.first()
        last_result = results.last()
        score_delta = None
        if first_result and last_result and first_result != last_result:
            score_delta = round(last_result.overall_score - first_result.overall_score, 1)

        practice_completions = PracticeCompletion.objects.filter(
            practice__couple=couple, created_at__gte=month_ago
        ).count()

        mediation_sessions = ConflictSession.objects.filter(
            couple=couple, created_at__gte=month_ago, status='complete'
        ).count()

        plan_completions = TaskCompletion.objects.filter(
            user__in=[couple.partner_a, couple.partner_b] if couple.partner_b else [couple.partner_a],
            created_at__gte=month_ago
        ).count()

        context = {
            'report': report,
            'couple': couple,
            'month': now.strftime('%B %Y'),
            'latest_result': last_result,
            'score_delta': score_delta,
            'practice_completions': practice_completions,
            'mediation_sessions': mediation_sessions,
            'plan_completions': plan_completions,
        }
        if last_result:
            from apps.analytics.services import AnalyticsService
            context['zones'] = AnalyticsService.get_zone_detail_for_result(last_result)
        return render_to_string('reports/monthly.html', context)

    @staticmethod
    def _upload_to_s3(pdf_bytes: bytes, key: str) -> None:
        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL or None,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=io.BytesIO(pdf_bytes),
            ContentType='application/pdf',
        )
