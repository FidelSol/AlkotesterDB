from django.contrib.auth.models import Group, Permission
from .permission_constants import *

def generate_groups_and_permission(content_type):
    groups = customuser_permission_group
    for k, v in groups.items():
        try:
            group_name = k
            group = Group.objects.get_or_create(name=group_name)
            for permission in v:
                permission_codename = permission[0]
                permission_name = permission[1]
                permission, created = Permission.objects.get_or_create(codename=permission_codename,
                                                                       name=permission_name,
                                                                       content_type=content_type)
                group[0].permissions.add(permission)
        except Exception as e:
            return e

