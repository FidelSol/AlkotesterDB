from django.contrib import admin

from .models import Personal, Photo, Tests, CustomUser

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


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

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'username', 'is_staff', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()




admin.site.register(Personal, PersonalAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tests, TestsAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)