from django.core.exceptions import PermissionDenied

def access_permissions(permission):
    """ django-rest-framework permission decorator for custom methods """

    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            user_permission = str(kwargs['pk'])+permission
            if self.request.user.has_perm(user_permission):
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()
        return _decorator
    return decorator




