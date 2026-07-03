from django.urls import path
from .views import (
    QuestionsView, SessionCreateView, CurrentSessionView,
    SaveAnswersView, CompleteSessionView, JourneyView,
)

urlpatterns = [
    path('journey/',                                       JourneyView.as_view()),
    path('questions/',                                     QuestionsView.as_view()),
    path('sessions/',                                      SessionCreateView.as_view()),
    path('sessions/current/',                              CurrentSessionView.as_view()),
    path('sessions/<uuid:session_id>/answers/',            SaveAnswersView.as_view()),
    path('sessions/<uuid:session_id>/complete/',           CompleteSessionView.as_view()),
]
