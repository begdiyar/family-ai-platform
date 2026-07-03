from django.contrib import admin

from .models import User, CommunicationPreference


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('email', 'first_name', 'last_name', 'gender', 'is_verified', 'is_active', 'created_at')
    list_filter   = ('is_active', 'is_verified', 'is_staff', 'gender', 'education_level')
    search_fields = ('email', 'first_name', 'last_name', 'occupation')
    ordering      = ('-created_at',)
    readonly_fields = ('id', 'password', 'last_login', 'created_at', 'updated_at')
    exclude       = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Личные данные', {'fields': (
            'first_name', 'last_name', 'birth_date',
            'gender', 'native_language', 'occupation', 'education_level',
            'avatar_url', 'preferred_language',
        )}),
        ('Статус', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser')}),
        ('Системное', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )


@admin.register(CommunicationPreference)
class CommunicationPreferenceAdmin(admin.ModelAdmin):
    list_display  = ('user', 'conflict_style', 'support_style', 'updated_at')
    list_filter   = ('conflict_style', 'support_style')
    search_fields = ('user__email', 'user__first_name')
    raw_id_fields = ('user',)
