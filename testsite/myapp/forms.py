from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


lab_choices = [
    ('lab1', 'lab1'),
    ('lab2', 'lab2'),
    ('lab3', 'lab3'),
]


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Wybierz plik')
    labName = forms.CharField(label="Wybierz nazwe labolatorium", widget=forms.Select(choices=lab_choices))


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