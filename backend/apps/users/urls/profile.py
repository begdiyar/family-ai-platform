from django.urls import path
from apps.users.views import MeView, CommunicationPreferenceView, ChangePasswordView

urlpatterns = [
    path('me/', MeView.as_view(), name='user-me'),
    path('me/communication-pref/', CommunicationPreferenceView.as_view(), name='user-communication-pref'),
    path('me/change-password/', ChangePasswordView.as_view(), name='user-change-password'),
]
