from typing import Optional, List
from django.utils import timezone
from apps.couples.models import Couple
from apps.users.models import User
from .models import Report


class ReportRepository:
    @staticmethod
    def create(couple: Couple, user: User, result, report_type: str) -> Report:
        return Report.objects.create(
            couple=couple,
            created_by=user,
            result=result,
            report_type=report_type,
        )

    @staticmethod
    def get_by_id(report_id, couple: Couple = None) -> Optional[Report]:
        qs = Report.objects.filter(id=report_id)
        if couple:
            qs = qs.filter(couple=couple)
        return qs.first()

    @staticmethod
    def list_for_couple(couple: Couple) -> List[Report]:
        return list(Report.objects.filter(couple=couple).order_by('-created_at'))

    @staticmethod
    def mark_ready(report: Report, file_url: str) -> None:
        report.status = Report.STATUS_READY
        report.file_url = file_url
        report.save(update_fields=['status', 'file_url', 'updated_at'])

    @staticmethod
    def mark_failed(report: Report) -> None:
        report.status = Report.STATUS_FAILED
        report.save(update_fields=['status', 'updated_at'])

    @staticmethod
    def set_share_token(report: Report, token: str, expires_at) -> None:
        report.share_token = token
        report.share_expires_at = expires_at
        report.save(update_fields=['share_token', 'share_expires_at', 'updated_at'])

    @staticmethod
    def get_by_share_token(token: str) -> Optional[Report]:
        return Report.objects.filter(
            share_token=token,
            share_expires_at__gt=timezone.now(),
        ).first()
