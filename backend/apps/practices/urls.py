from django.urls import path
from .views import (
    TodayPracticeView, CompleteSlotView,
    FamilyPlanView, PracticeStatsView, PracticeHistoryView,
)

urlpatterns = [
    path('today/',                                     TodayPracticeView.as_view()),
    path('plan/',                                      FamilyPlanView.as_view()),
    path('<uuid:assignment_id>/complete/<str:slot>/',  CompleteSlotView.as_view()),
    path('stats/',                                     PracticeStatsView.as_view()),
    path('history/',                                   PracticeHistoryView.as_view()),
]
