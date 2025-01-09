from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Lead, Agent, UserProfile, Category





# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (None, {"fields": ("is_organisor", "is_agent")}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Category)
admin.site.register(Agent)