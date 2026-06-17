from django.urls import path
from .views import ConflictSessionListView, ConflictSessionDetailView, SubmitEntryView

urlpatterns = [
    path('', ConflictSessionListView.as_view()),
    path('<uuid:session_id>/', ConflictSessionDetailView.as_view()),
    path('<uuid:session_id>/submit/', SubmitEntryView.as_view()),
]
