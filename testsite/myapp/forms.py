from django import forms
from .models import LabChoice, OneTimeCode
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    labName = forms.ModelChoiceField(
        label="Choose lab number",
        queryset=LabChoice.objects.all(),
        widget=forms.Select,
        to_field_name='name'
    )



class LabChoiceForm(forms.Form):
    labname = forms.CharField(label="Lab Name", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter lab name'}))
    template_file = forms.FileField(label='Upload Lab Template')

    def clean_labname(self):
        labname = self.cleaned_data['labname']
        # Ensure safe directory name
        if not re.match(r'^[a-zA-Z0-9_-]+$', labname):
            raise ValidationError(
                'Lab name can only contain letters, numbers, underscores and hyphens'
            )
        return labname


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    one_time_code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your one-time code'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'one_time_code']

    def clean_one_time_code(self):
        one_time_code = self.cleaned_data['one_time_code']
        try:
            code_obj = OneTimeCode.get_by_raw_code(one_time_code)
            if code_obj.is_used:
                raise forms.ValidationError("This code has already been used.")
        except OneTimeCode.DoesNotExist:
            raise forms.ValidationError("Invalid one-time code.")
        return one_time_code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Mark the one-time code as used
            code_obj = OneTimeCode.get_by_raw_code(self.cleaned_data['one_time_code'])
            code_obj.mark_as_used()
        return user