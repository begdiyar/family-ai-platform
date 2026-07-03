from django.urls import path
from .views import (
    CoupleCreateView, CoupleDetailView,
    InviteAcceptView, InviteRegenerateView,
    ChildrenView, ChildDetailView,
    FamilyContextView,
    FamilyValuesListView, CoupleFamilyValuesView,
)

urlpatterns = [
    # Core couple
    path('', CoupleCreateView.as_view(), name='couple-create'),
    path('me/', CoupleDetailView.as_view(), name='couple-detail'),
    path('invite/accept/', InviteAcceptView.as_view(), name='couple-invite-accept'),
    path('invite/regenerate/', InviteRegenerateView.as_view(), name='couple-invite-regenerate'),

    # Children
    path('me/children/', ChildrenView.as_view(), name='couple-children'),
    path('me/children/<uuid:child_id>/', ChildDetailView.as_view(), name='couple-child-detail'),

    # Family context (relationship + cohabitation + influence)
    path('me/family-context/', FamilyContextView.as_view(), name='couple-family-context'),

    # Family values
    path('me/family-values/', CoupleFamilyValuesView.as_view(), name='couple-family-values'),
    path('family-values/', FamilyValuesListView.as_view(), name='family-values-list'),
]
