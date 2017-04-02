from django import forms


class RegForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.CharField(max_length=30)
    tel = forms.CharField(max_length=13)
    password = forms.CharField(max_length=20)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20)


class ChangeForm(forms.Form):
    email = forms.CharField(max_length=30)
    tel = forms.CharField(max_length=13)

