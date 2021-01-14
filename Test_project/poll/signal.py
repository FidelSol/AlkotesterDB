from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import generate_groups_and_permission
from django.contrib.contenttypes.models import ContentType
from .permission_constants import *
from django.contrib.auth.models import Group, User


@receiver(post_save, sender=User)
def create_groups_for_project(sender, instance, **kwargs):
    if kwargs['created']:
        try:
            content_type = ContentType.objects.get(model=instance._meta.model_name)
            generate_groups_and_permission(instance._meta.model_name,
                                           str(instance.id), content_type)

            super_group = Group.objects.get(name=str(instance.id) + '-' + SUPER_GROUP)
            view_group = Group.objects.get(name=str(instance.id) + '-' + VIEW_ONLY_GROUP)

            User.groups.add(super_group)

        except Exception as e:
            raise e
    else:
        print("Object not created yet.")




