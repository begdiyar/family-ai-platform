from django.urls import path
from .views import ConversationListCreateView, MessageListView, MessageStreamView

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='ai-conversations'),
    path('conversations/<uuid:conv_id>/messages/', MessageListView.as_view(), name='ai-messages-list'),
    path('conversations/<uuid:conv_id>/messages/send/', MessageStreamView.as_view(), name='ai-messages-send'),
]
