from django import forms


lab_choices = [
    ('lab1', 'lab1'),
    ('lab2', 'lab2'),
    ('lab3', 'lab3'),
]


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    labName = forms.CharField(label="Choose lab number", widget=forms.Select(choices=lab_choices))
