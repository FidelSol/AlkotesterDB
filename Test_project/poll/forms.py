
from django import forms
from .models import Tests, Photo


class TestsForm(forms.ModelForm):
    expected_time = forms.DateTimeField(label='Назначенное время сдачи теста:', input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}))
    result_time = forms.DateTimeField(label='Фактическое время сдачи теста:', input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker2'}))

    class Meta:
        model = Tests
        fields = ('expected_time', 'result_time')

class PhotoForm(forms.ModelForm):
    data_photo = forms.ImageField(label='Фото')

    class Meta:
        model = Photo
        fields = ( 'data_photo', )