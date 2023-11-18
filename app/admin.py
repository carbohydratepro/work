from django.contrib import admin
from .models import Shift

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('user', 'applicant_name', 'substitute_user', 'confirmed_user', 'date', 'start_time', 'end_time', 'is_substitute_found', 'is_confirmed', 'position')
    list_filter = ('date', 'is_substitute_found', 'is_confirmed', 'position')
    search_fields = ('applicant_name', 'substitute_name', 'memo')
    ordering = ('date', 'start_time')

    # 任意：Shift モデルの詳細ページでのフィールドセット
    fieldsets = (
        (None, {'fields': ('user', 'applicant_name', 'substitute_user', 'substitute_name')}),
        ('シフト情報', {'fields': ('date', 'start_time', 'end_time', 'position', 'memo')}),
        ('ステータス', {'fields': ('is_substitute_found', 'is_confirmed', 'is_staff', 'is_myself')}),
    )

admin.site.register(Shift, ShiftAdmin)
