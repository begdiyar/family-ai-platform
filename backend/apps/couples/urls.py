from django.urls import path
from .views import CoupleCreateView, CoupleDetailView, InviteAcceptView, InviteRegenerateView

urlpatterns = [
    path('', CoupleCreateView.as_view(), name='couple-create'),
    path('me/', CoupleDetailView.as_view(), name='couple-detail'),
    path('invite/accept/', InviteAcceptView.as_view(), name='couple-invite-accept'),
    path('invite/regenerate/', InviteRegenerateView.as_view(), name='couple-invite-regenerate'),
]
