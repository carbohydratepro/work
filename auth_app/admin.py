from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser

class CustomUserAdmin(DefaultUserAdmin):
    model = CustomUser
    list_display = ('employee_id_number', 'username', 'email', 'position', 'store_code', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'position')
    fieldsets = (
        (None, {'fields': ('employee_id_number', 'password')}),
        ('Personal info', {'fields': ('username', 'email', 'position', 'store_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_id_number', 'username', 'email', 'position', 'store_code', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('employee_id_number', 'username', 'email')
    ordering = ('employee_id_number',)

admin.site.register(CustomUser, CustomUserAdmin)
