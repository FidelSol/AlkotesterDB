from __future__ import absolute_import
from django.core.exceptions import PermissionDenied
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


def access_permissions(permission):
    """ django-rest-framework permission decorator for custom methods """

    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            user_permission = 'auth.' + permission[0]
            user = get_current_user()
            mn = user.get_group_permissions()
            if user_permission in mn:
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()
        return _decorator
    return decorator






