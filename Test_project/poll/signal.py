from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from .utils import generate_groups_and_permission
from django.contrib.contenttypes.models import ContentType
from .permission_constants import *
from django.contrib.auth.models import Group

@receiver(post_save, sender=CustomUser)
def create_groups_for_project(CustomUser, instance, **kwargs):
    c = CustomUser.objects.last()
    try:
        content_type = ContentType.objects.get(model=c._meta.model_name)
        generate_groups_and_permission(c._meta.model_name, str(c.id), content_type)
        super_group = Group.objects.get(name=str(c.id) + '-' + CUSTOMUSER_SUPER_GROUP)
        c.groups.add(super_group)
        super_group.user_set.add(c)
    except Exception as e:
        raise e




