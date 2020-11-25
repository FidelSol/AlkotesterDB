
from .models import Tests
from django import forms
from datetimewidget.widgets import DateTimeWidget


class TestsForm(forms.ModelForm):
    expected_time = forms.DateTimeField(widget=forms.DateTimeInput)
    result_time = forms.DateTimeField(widget=forms.DateTimeInput)

    class Meta:
        model = Tests
        fields = ('expected_time', 'result_time')
        widgets = {'expected_time': DateTimeWidget(attrs={'id': "expected_time"}, usel10n=True, bootstrap_version=4), 'result_time': DateTimeWidget(attrs={'id': "result_time"}, usel10n=True, bootstrap_version=4)
        }


