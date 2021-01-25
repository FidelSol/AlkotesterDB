from django import template

register = template.Library()

@register.filter(name='has_permission')
def has_permission(user, permission):
    perms = user.get_group_permissions()
    return permission in perms