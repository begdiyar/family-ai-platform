from django.contrib import admin
from .models import CoachConversation, CoachMessage


class CoachMessageInline(admin.TabularInline):
    model          = CoachMessage
    fields         = ['role', 'content', 'tokens_used', 'created_at']
    readonly_fields = ['created_at']
    extra          = 0
    ordering       = ['created_at']


@admin.register(CoachConversation)
class CoachConversationAdmin(admin.ModelAdmin):
    list_display   = ['user', 'couple', 'dialog_type', 'title', 'created_at']
    list_filter    = ['dialog_type', 'created_at']
    search_fields  = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines        = [CoachMessageInline]
    ordering       = ['-created_at']


@admin.register(CoachMessage)
class CoachMessageAdmin(admin.ModelAdmin):
    list_display   = ['conversation', 'role', 'preview', 'tokens_used', 'created_at']
    list_filter    = ['role', 'created_at']
    search_fields  = ['content', 'conversation__user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering       = ['-created_at']

    @admin.display(description='Содержание')
    def preview(self, obj):
        return obj.content[:80] + '…' if len(obj.content) > 80 else obj.content
