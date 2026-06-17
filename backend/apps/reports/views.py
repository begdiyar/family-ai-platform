from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from shared.exceptions import NotFoundError
from apps.couples.repositories import CoupleRepository
from .models import Report
from .repositories import ReportRepository
from .serializers import ReportSerializer, CreateReportSerializer, ShareSerializer
from .services import ReportService


class ReportListCreateView(APIView):
    def get(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise NotFoundError('NO_COUPLE', 'Нет активной пары')
        reports = ReportRepository.list_for_couple(couple)
        data = ReportSerializer(reports, many=True).data
        return Response({'count': len(data), 'results': data})

    def post(self, request):
        serializer = CreateReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = ReportService.create_report(
            user=request.user,
            report_type=serializer.validated_data['report_type'],
            result_id=str(serializer.validated_data.get('result_id', '') or ''),
        )
        return Response(ReportSerializer(report).data, status=status.HTTP_202_ACCEPTED)


class ReportDetailView(APIView):
    def get(self, request, report_id):
        couple = CoupleRepository.get_active_for_user(request.user)
        report = ReportRepository.get_by_id(report_id, couple)
        if not report:
            raise NotFoundError('REPORT_NOT_FOUND', 'Отчёт не найден')
        return Response(ReportSerializer(report).data)


class ReportShareView(APIView):
    def post(self, request, report_id):
        share_data = ReportService.create_share_link(request.user, str(report_id))
        return Response(ShareSerializer(share_data).data)


class ReportDownloadView(APIView):
    def get(self, request, report_id):
        couple = CoupleRepository.get_active_for_user(request.user)
        report = ReportRepository.get_by_id(report_id, couple)
        if not report or not report.file_url:
            raise NotFoundError('REPORT_NOT_READY', 'Файл ещё не готов')
        url = report.file_url.replace('http://minio:9000', 'http://localhost:9000')
        return Response({'download_url': url})


class SharedReportView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        report = ReportService.get_shared_report(token)
        return Response(ReportSerializer(report).data)
