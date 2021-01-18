from django.core.serializers import serialize
import json
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError

from .permission_constants import *

PERMISSION_GROUP_SUFFIX = '_permission_group'
current_module_variables = vars()

def generate_groups_and_permission(model_name, content_type):
    groups = current_module_variables[model_name + PERMISSION_GROUP_SUFFIX]
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
                group.permissions.add(permission)
        except Exception as e:
            return e

def serialize_bootstraptable(queryset):
    json_data = serialize('json', queryset)
    json_final = {"total": queryset.count(), "rows": []}
    data = json.loads(json_data)
    for item in data:
        del item["model"]
        item["fields"].update({"id": item["pk"]})
        item = item["fields"]
        json_final['rows'].append(item)
    return json_final