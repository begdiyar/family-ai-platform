from django.urls import path
from .views import QuestionsView, SessionCreateView, CurrentSessionView, SaveAnswersView, CompleteSessionView

urlpatterns = [
    path('questions/', QuestionsView.as_view(), name='diagnostics-questions'),
    path('sessions/', SessionCreateView.as_view(), name='diagnostics-session-create'),
    path('sessions/current/', CurrentSessionView.as_view(), name='diagnostics-session-current'),
    path('sessions/<uuid:session_id>/answers/', SaveAnswersView.as_view(), name='diagnostics-save-answers'),
    path('sessions/<uuid:session_id>/complete/', CompleteSessionView.as_view(), name='diagnostics-complete'),
]
