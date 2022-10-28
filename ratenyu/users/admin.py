from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin
from .models import UserDetails


class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = "UserDetails"


class CustomUserAdmin(UserAdmin):
    inlines = (UserDetailsInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
