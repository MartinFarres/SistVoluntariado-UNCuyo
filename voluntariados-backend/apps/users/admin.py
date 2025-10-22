from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from simple_history.admin import SimpleHistoryAdmin


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", "role", "persona")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "persona", "is_active", "is_staff"),
        }),
    )
    list_display = ("email", "role", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(User.history.model)
class HistoricalUserAdmin(SimpleHistoryAdmin):
    list_display = ("id", "email", "role", "history_date", "history_user", "history_type")
    search_fields = ("email", "history_user__email")
