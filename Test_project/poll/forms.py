from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
from .models import Tests, Photo, Personal, CustomUser


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'role')

class PersonalForm(forms.ModelForm):
    birth_date = forms.DateField(label='Дата рождения:')

    class Meta:
        model = Personal
        fields = ('ext_id', 'full_name', 'birth_date', 'position', 'punishment')

class TestsForm(forms.ModelForm):
    expected_time = forms.DateTimeField(label='Назначенное время сдачи теста:', input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}))
    result_time = forms.DateTimeField(label='Фактическое время сдачи теста:', input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker2'}))

    class Meta:
        model = Tests
        fields = ('expected_time', 'result_time', 'result')

class PhotoForm(forms.ModelForm):


    class Meta:
        model = Photo
        fields = ( '__all__' )

PhotoFormSet = inlineformset_factory(Personal, Photo, form=PhotoForm, extra=1, can_delete=True)


