from django.contrib import admin

from .models import Couple, CoupleInvite, Child, FamilyValue


class ChildInline(admin.TabularInline):
    model  = Child
    extra  = 0
    fields = ('birth_date', 'gender')


@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):
    list_display  = (
        '__str__', 'status', 'relationship_status',
        'relationship_start_date', 'lives_with_parents', 'created_at',
    )
    list_filter   = ('status', 'relationship_status', 'lives_with_parents')
    search_fields = ('partner_a__email', 'partner_b__email')
    raw_id_fields = ('partner_a', 'partner_b')
    filter_horizontal = ('family_values',)
    inlines       = [ChildInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('partner_a', 'partner_b', 'status')}),
        ('Отношения', {'fields': (
            'relationship_status', 'relationship_start_date', 'marriage_date', 'marriage_year',
        )}),
        ('Дети (legacy)', {'fields': ('has_children', 'children_count')}),
        ('Семейный контекст', {'fields': (
            'lives_with_parents', 'relatives_influence_level', 'religious_traditions_importance',
        )}),
        ('Ценности', {'fields': ('family_values',)}),
    )


@admin.register(CoupleInvite)
class CoupleInviteAdmin(admin.ModelAdmin):
    list_display  = ('token', 'couple', 'status', 'expires_at')
    list_filter   = ('status',)
    search_fields = ('token', 'couple__partner_a__email')
    raw_id_fields = ('couple', 'invited_by')


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display  = ('couple', 'birth_date', 'gender', 'created_at')
    list_filter   = ('gender',)
    search_fields = ('couple__partner_a__email',)
    raw_id_fields = ('couple',)


@admin.register(FamilyValue)
class FamilyValueAdmin(admin.ModelAdmin):
    list_display  = ('slug', 'label_ru')
    search_fields = ('slug', 'label_ru')
