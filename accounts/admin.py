from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("employee_id", "role", "department", "is_staff")
    fieldsets = (
        (None, {"fields": ("employee_id", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Role & Department", {"fields": ("role", "department")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("employee_id", "password1", "password2", "role", "department"),
        }),
    )
    ordering = ("employee_id",)


admin.site.register(User, CustomUserAdmin)
