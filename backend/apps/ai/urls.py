from django.urls import path
from .views import CoachView, MediatorView

urlpatterns = [
    path('coach/',    CoachView.as_view(),    name='ai-coach'),
    path('mediator/', MediatorView.as_view(), name='ai-mediator'),
]
