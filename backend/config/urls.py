from django.urls import path, include
from shared.views import HealthCheckView

urlpatterns = [
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/auth/', include('apps.users.urls.auth')),
    path('api/v1/users/', include('apps.users.urls.profile')),
    path('api/v1/couples/', include('apps.couples.urls')),
    path('api/v1/diagnostics/', include('apps.diagnostics.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/ai/', include('apps.ai_consultant.urls')),
    path('api/v1/plans/', include('apps.plans.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/mediation/', include('apps.mediation.urls')),
    path('api/v1/constitution/', include('apps.constitution.urls')),
    path('api/v1/practices/', include('apps.practices.urls')),
    path('api/v1/academy/', include('apps.academy.urls')),
]
