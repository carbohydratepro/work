from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'position', 'store_code', 'employee_id_number')  # ここを変更
    # ユーザー作成時のフィールドセットを調整
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    # ユーザー編集時のフィールドセットを調整
    fieldsets = (
        (None, {'fields': ('employee_id_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
