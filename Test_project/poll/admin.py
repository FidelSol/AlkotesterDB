from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Personal, Photo, Tests, CustomUser, CHIEF, REVIZOR
from .utils import generate_groups_and_permission


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'role', 'last_name', 'first_name',
                    'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
                'first_name', 'last_name', 'email', 'role'
            )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role')}
         ),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
        content_type = ContentType.objects.get(model=obj._meta.model_name)
        generate_groups_and_permission(obj._meta.model_name, content_type)
        if obj.role == CHIEF:
            group = Group.objects.get(name='_customuser_super_group')
        elif obj.role == REVIZOR:
            group = Group.objects.get(name='_customuser_document_management_group')
        else:
            group = Group.objects.get(name='_customuser_view_only_group')
        group.user_set.add(obj)


# Register your models here.

class PersonalAdmin(admin.ModelAdmin):
    list_display = ('personal_id', 'ext_id', 'full_name')
    list_display_links = ('personal_id', 'ext_id', 'full_name')
    search_fields = ('personal_id', 'ext_id', 'full_name')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_id', 'personal', 'data_pub', 'data_photo')
    list_display_links = ('photo_id', 'personal', 'data_pub', 'data_photo')
    search_fields = ('photo_id', 'personal', 'data_pub', 'data_photo')

class TestsAdmin(admin.ModelAdmin):
    list_display = ('tests_id', 'personal', 'expected_time', 'result_time')
    list_display_links = ('tests_id', 'personal', 'expected_time', 'result_time')
    search_fields = ('tests_id', 'personal', 'expected_time', 'result_time')



admin.site.register(Personal, PersonalAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tests, TestsAdmin)
admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)


