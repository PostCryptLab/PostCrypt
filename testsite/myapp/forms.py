from django import forms
from .models import LabChoice
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


lab_choices = [
    ('lab1', 'lab1'),
    ('lab2', 'lab2'),
    ('lab3', 'lab3'),
]


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    labName = forms.ModelChoiceField(
        label="Choose lab number",
        queryset=LabChoice.objects.all(),
        widget=forms.Select
    )

class LabChoiceForm(forms.Form):

    labname = forms.CharField(label="Lab Name", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter lab name'}))


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user