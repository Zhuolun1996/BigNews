from django import forms

class FileForm(forms.Form):
    key=forms.CharField(max_length=100)
