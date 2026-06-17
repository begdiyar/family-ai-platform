from django.urls import path
from .views import ConstitutionView, ConstitutionGenerateView

urlpatterns = [
    path('', ConstitutionView.as_view()),
    path('generate/', ConstitutionGenerateView.as_view()),
]
