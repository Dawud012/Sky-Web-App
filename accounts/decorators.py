# Author : Parham Golmohammadi

from functools import wraps
from django.core.exceptions import PermissionDenied

def restrict_to_roles(*roles):
    def outer(fn):
        @wraps(fn)
        def inner(request, *args, **kwargs):
            prof = getattr(request.user, 'profile', None)
            if prof and prof.role in roles:
                return fn(request, *args, **kwargs)
            raise PermissionDenied
        return inner
    return outer