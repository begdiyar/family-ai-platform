from django.urls import path
from .views import (
    AdminOverviewView,
    AdminRegistrationsView,
    AdminActivityView,
    AdminFamiliesView,
    AdminFamilyDetailView,
    AdminProblemsView,
    AdminTrendsView,
    AdminExportView,
)

urlpatterns = [
    path('overview/', AdminOverviewView.as_view(), name='admin-overview'),
    path('registrations/', AdminRegistrationsView.as_view(), name='admin-registrations'),
    path('activity/', AdminActivityView.as_view(), name='admin-activity'),
    path('trends/', AdminTrendsView.as_view(), name='admin-trends'),
    path('families/', AdminFamiliesView.as_view(), name='admin-families'),
    path('families/<uuid:couple_id>/', AdminFamilyDetailView.as_view(), name='admin-family-detail'),
    path('problems/', AdminProblemsView.as_view(), name='admin-problems'),
    path('export/', AdminExportView.as_view(), name='admin-export'),
]
