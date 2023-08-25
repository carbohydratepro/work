from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username',)  # ここを変更
    # ユーザー作成時のフィールドセットを調整
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    # ユーザー編集時のフィールドセットを調整
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
