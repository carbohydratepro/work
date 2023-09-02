from django import forms
from .models import Shift

class ShiftForm(forms.ModelForm):

    HOURS = [i for i in range(5, 23)]  # 5 to 22
    MINUTES = [0, 10, 20, 30, 40, 50]

    HOUR_CHOICES = [(f"{hour:02d}", f"{hour:02d}") for hour in HOURS]
    MINUTE_CHOICES = [(f"{minute:02d}", f"{minute:02d}") for minute in MINUTES]

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    start_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='開始時')
    start_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='開始分')
    end_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='終了時')
    end_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='終了分')

    class Meta:
        model = Shift
        fields = ['applicant_name', 'substitute_name', 'date', 'start_hour', 'start_minute', 'end_hour', 'end_minute', 'is_substitute_found']
