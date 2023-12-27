from django.contrib import admin
from .models import Shift, RegisteredShift, Break

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

class RegisteredShiftAdmin(admin.ModelAdmin):
    list_display = ('username', 'date', 'start_time', 'end_time', 'position')
    list_filter = ('date', 'position')
    search_fields = ('username',)

class BreakAdmin(admin.ModelAdmin):
    list_display = ('shift', 'start_time', 'end_time')
    list_filter = ('shift__date', 'shift__username')
    search_fields = ('shift__username',)
    
admin.site.register(Shift, ShiftAdmin)
admin.site.register(RegisteredShift, RegisteredShiftAdmin)
admin.site.register(Break, BreakAdmin)