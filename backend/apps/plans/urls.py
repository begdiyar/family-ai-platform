from django.urls import path
from .views import PlanCreateView, PlanCurrentView, TaskCompleteView

urlpatterns = [
    path('', PlanCreateView.as_view(), name='plan-create'),
    path('current/', PlanCurrentView.as_view(), name='plan-current'),
    path('<uuid:plan_id>/tasks/<uuid:task_id>/complete/', TaskCompleteView.as_view(), name='task-complete'),
]
