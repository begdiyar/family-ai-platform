from django.urls import path
from .views import ReportListCreateView, ReportDetailView, ReportShareView, ReportDownloadView, SharedReportView

urlpatterns = [
    path('', ReportListCreateView.as_view(), name='report-list-create'),
    path('<uuid:report_id>/', ReportDetailView.as_view(), name='report-detail'),
    path('<uuid:report_id>/download/', ReportDownloadView.as_view(), name='report-download'),
    path('<uuid:report_id>/share/', ReportShareView.as_view(), name='report-share'),
    path('shared/<str:token>/', SharedReportView.as_view(), name='report-shared'),
]
