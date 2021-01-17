from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from .utils import generate_groups_and_permission
from django.contrib.contenttypes.models import ContentType
from .permission_constants import *
from django.contrib.auth.models import Group

@receiver(post_save, sender=CustomUser)
def create_groups_for_project(CustomUser, instance, **kwargs):
    if kwargs['created']:
        try:
            content_type = ContentType.objects.get(model=instance._meta.model_name)
            generate_groups_and_permission(instance._meta.model_name,
                                           str(instance.id), content_type)

            super_group = Group.objects.get(name=str(instance.id) + '-' + CUSTOMUSER_SUPER_GROUP)



            instance.groups.add(super_group)

        except Exception as e:
            raise e
    else:
        print("Object not created yet.")



