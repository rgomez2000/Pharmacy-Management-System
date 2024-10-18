from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'userprofile__is_locked', 'userprofile__failed_login_attempts')

    # This method overrides the default save_model method to reset failed_login_attempts to 0
    # any time this user is changed and the value of `is_locked` is False.
    def save_model(self, request, obj, form, change):
        if not obj.userprofile.is_locked:
            obj.userprofile.failed_login_attempts = 0
        super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
