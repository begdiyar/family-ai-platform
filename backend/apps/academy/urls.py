from django.urls import path
from .views import (
    ArticleListView, ArticleDetailView, ArticleCompleteView, ArticleReflectView,
    TrainingListView, TrainingDetailView, TrainingStartView, TrainingCompleteView,
    ProgramListView, ProgramDetailView, ProgramEnrollView, ProgramDayCompleteView,
    MicroPracticeTodayView, MicroPracticeCompleteView,
    LearningProgressView, RecommendationsView, AchievementsView, ActiveProgramView,
)

urlpatterns = [
    # Articles
    path('articles/', ArticleListView.as_view(), name='academy-articles'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='academy-article-detail'),
    path('articles/<slug:slug>/complete/', ArticleCompleteView.as_view(), name='academy-article-complete'),
    path('articles/<slug:slug>/reflect/', ArticleReflectView.as_view(), name='academy-article-reflect'),

    # Trainings
    path('trainings/', TrainingListView.as_view(), name='academy-trainings'),
    path('trainings/<slug:slug>/', TrainingDetailView.as_view(), name='academy-training-detail'),
    path('trainings/<slug:slug>/start/', TrainingStartView.as_view(), name='academy-training-start'),
    path('trainings/<slug:slug>/complete/', TrainingCompleteView.as_view(), name='academy-training-complete'),

    # Programs
    path('programs/', ProgramListView.as_view(), name='academy-programs'),
    path('programs/active/', ActiveProgramView.as_view(), name='academy-program-active'),
    path('programs/<slug:slug>/', ProgramDetailView.as_view(), name='academy-program-detail'),
    path('programs/<slug:slug>/enroll/', ProgramEnrollView.as_view(), name='academy-program-enroll'),
    path('programs/<slug:slug>/days/<int:day_number>/complete/', ProgramDayCompleteView.as_view(), name='academy-day-complete'),

    # Micro practice
    path('micro-practice/today/', MicroPracticeTodayView.as_view(), name='academy-micro-today'),
    path('micro-practice/<uuid:practice_id>/complete/', MicroPracticeCompleteView.as_view(), name='academy-micro-complete'),

    # Progress & recommendations
    path('progress/', LearningProgressView.as_view(), name='academy-progress'),
    path('recommendations/', RecommendationsView.as_view(), name='academy-recommendations'),
    path('achievements/', AchievementsView.as_view(), name='academy-achievements'),
]
