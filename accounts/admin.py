from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'userprofile__is_locked', 'userprofile__failed_login_attempts')

    def unlock_users(self, request, queryset):
        # Check if the user has the 'can_unlock_users' permission
        if not request.user.has_perm('accounts.can_unlock_users'):
            self.message_user(request, "You do not have permission to unlock accounts.", level='error')
            return
        
        for user in queryset:
            user.userprofile.is_locked = False
            user.userprofile.failed_login_attempts = 0
            user.userprofile.save()
        self.message_user(request, "Selected users have been unlocked.")

    unlock_users.short_description = "Unlock selected users"

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Hide the action if the user does not have the permission
        if not request.user.has_perm('accounts.can_unlock_users'):
            actions.pop('unlock_users', None)
        return actions

def create_unlock_permission():
    content_type = ContentType.objects.get_for_model(UserProfile)
    Permission.objects.get_or_create(
        codename='can_unlock_users',
        name='Can unlock user accounts',
        content_type=content_type,
    )

# Creating the permission if it doesn't exist
create_unlock_permission()

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

