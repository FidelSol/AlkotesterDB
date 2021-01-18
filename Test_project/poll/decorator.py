
from django.core.exceptions import PermissionDenied
from django_currentuser.middleware import (
get_current_user, get_current_authenticated_user)


def access_permissions(permission):
    """ django-rest-framework permission decorator for custom methods """

    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            user_permission = permission
            user = get_current_user()
            if user.has_perm(user_permission):
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()
        return _decorator
    return decorator

user = get_current_authenticated_user()

def access(permission):

    def decorator(permission):
        user_permission = permission
        if user.has_perm(user_permission):
            return decorator()
        else:
            raise PermissionDenied()
    return decorator


