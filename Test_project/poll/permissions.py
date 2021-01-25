from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class ChiefPermissions(permissions.BasePermission):
    allowed_group_permissions = ('poll.add_personal')

    def has_permission(self, request, view):
        self.user = request.user
        self.mn = self.user.get_group_permissions()
        is_allowed_user = self.allowed_group_permissions in self.mn
        return is_allowed_user

class ChiefAndRevizorPermissions(permissions.BasePermission):
    allowed_group_permissions = {'poll.add_personal', 'poll.add_tests'}

    def has_permission(self, request, view):
        is_allowed_user = True
        user = request.user
        mn = user.get_group_permissions()
        for p in mn:
            if p in self.allowed_group_permissions:
                is_allowed_user = True
                break
            else:
                is_allowed_user = False
        return is_allowed_user

