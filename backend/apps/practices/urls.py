from django.urls import path
from .views import TodayPracticeView, CompletePracticeView

urlpatterns = [
    path('today/', TodayPracticeView.as_view()),
    path('<uuid:practice_id>/complete/', CompletePracticeView.as_view()),
]
