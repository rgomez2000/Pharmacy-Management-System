from django.http import HttpResponseForbidden
from functools import wraps

def pharmacist_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('med_inventory.can_check_inventory'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view