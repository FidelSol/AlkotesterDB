
from django import forms
from .models import Tests


class TestsForm(forms.ModelForm):
    expected_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}))
    result_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker2'}))

    class Meta:
        model = Tests
        fields = ('expected_time', 'result_time')