from django import forms

class User(forms.Form):
    username=forms.CharField(label='用户名',max_length=50)
    password=forms.CharField(label='密码',widget=forms.PasswordInput())