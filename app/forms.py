from django import forms
from .models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['applicant_name', 'substitute_name', 'start_time', 'end_time', 'is_substitute_found']
