from django.urls import path
from .views import (
    AnalyticsResultListView, AnalyticsResultLatestView,
    AnalyticsResultDetailView, AnalyticsProgressView,
)

urlpatterns = [
    path('results/', AnalyticsResultListView.as_view(), name='analytics-list'),
    path('results/latest/', AnalyticsResultLatestView.as_view(), name='analytics-latest'),
    path('results/<uuid:result_id>/', AnalyticsResultDetailView.as_view(), name='analytics-detail'),
    path('progress/', AnalyticsProgressView.as_view(), name='analytics-progress'),
]
