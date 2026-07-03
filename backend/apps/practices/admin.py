from django.contrib import admin
from django.db.models import Count
from .models import Practice, DailyAssignment, AssignmentSlot


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display    = ['title', 'category', 'slot_type', 'difficulty', 'duration_minutes', 'is_active', 'usage_count']
    list_filter     = ['category', 'slot_type', 'difficulty', 'is_active']
    list_editable   = ['is_active']
    search_fields   = ['title', 'description', 'tags']
    ordering        = ['category', 'slot_type', 'difficulty', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Содержание',     {'fields': ['title', 'description', 'instructions']}),
        ('Классификация',  {'fields': ['category', 'slot_type', 'difficulty', 'duration_minutes']}),
        ('Метаданные',     {'fields': ['tags', 'is_active']}),
        ('Академия',       {'fields': ['academy_article'], 'description': 'Для слота growth: статья Академии, к которой переходит пользователь'}),
        ('Переводы',       {'fields': ['i18n']}),
        ('Системное',      {'fields': ['id', 'created_at', 'updated_at'], 'classes': ['collapse']}),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_usage=Count('slots'))

    def usage_count(self, obj):
        return obj._usage
    usage_count.short_description = 'Использований'
    usage_count.admin_order_field = '_usage'


class AssignmentSlotInline(admin.TabularInline):
    model          = AssignmentSlot
    extra          = 0
    readonly_fields = ['slot_type', 'practice', 'completed', 'completed_at']
    can_delete     = False


@admin.register(DailyAssignment)
class DailyAssignmentAdmin(admin.ModelAdmin):
    list_display    = ['couple', 'date', 'completed_count', 'is_fully_completed', 'categories_used']
    list_filter     = ['date']
    readonly_fields = ['id', 'couple', 'date', 'categories_used', 'created_at', 'updated_at']
    ordering        = ['-date']
    date_hierarchy  = 'date'
    inlines         = [AssignmentSlotInline]


@admin.register(AssignmentSlot)
class AssignmentSlotAdmin(admin.ModelAdmin):
    list_display    = ['assignment', 'slot_type', 'practice', 'completed', 'completed_at']
    list_filter     = ['slot_type', 'completed']
    readonly_fields = ['id', 'assignment', 'completed_at', 'created_at', 'updated_at']
    ordering        = ['-assignment__date', 'slot_type']
