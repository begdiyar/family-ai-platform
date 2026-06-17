from django.utils import timezone
from datetime import timedelta

from shared.exceptions import NotFoundError, BusinessLogicError
from shared.utils import generate_token
from apps.couples.repositories import CoupleRepository
from apps.analytics.repositories import AnalyticsRepository
from apps.users.models import User
from .models import Report
from .repositories import ReportRepository


class ReportService:
    @staticmethod
    def create_report(user: User, report_type: str, result_id: str = None) -> Report:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')

        result = None
        if result_id:
            result = AnalyticsRepository.get_by_id(result_id)
        elif report_type == Report.TYPE_DIAGNOSTIC:
            result = AnalyticsRepository.get_latest_for_couple(couple)

        report = ReportRepository.create(
            couple=couple, user=user, result=result, report_type=report_type
        )

        from .tasks import generate_pdf_report
        generate_pdf_report.delay(str(report.id))

        return report

    @staticmethod
    def create_share_link(user: User, report_id: str) -> dict:
        couple = CoupleRepository.get_active_for_user(user)
        report = ReportRepository.get_by_id(report_id, couple)
        if not report:
            raise NotFoundError('REPORT_NOT_FOUND', 'Отчёт не найден')

        token = generate_token(32)
        expires_at = timezone.now() + timedelta(days=7)
        ReportRepository.set_share_token(report, token, expires_at)

        from django.conf import settings
        return {
            'share_token': token,
            'share_url': f"{settings.FRONTEND_URL}/shared/{token}",
            'expires_at': expires_at,
        }

    @staticmethod
    def get_shared_report(token: str) -> Report:
        report = ReportRepository.get_by_share_token(token)
        if not report:
            raise NotFoundError('SHARE_LINK_NOT_FOUND', 'Ссылка не найдена или истекла')
        if report.share_expires_at and report.share_expires_at < timezone.now():
            raise NotFoundError('SHARE_LINK_EXPIRED', 'Срок действия ссылки истёк')
        return report
