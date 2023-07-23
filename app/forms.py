from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    isadmin = forms.BooleanField(required=False)

class AdminForm(forms.Form):
    uid = forms.UUIDField(required=False)
    add = forms.CharField(max_length=10, required=False)
    remove = forms.CharField(max_length=10, required=False)

class EntryForm(forms.Form):
    uid = forms.UUIDField()
    absent = forms.CharField(max_length=30, required=False)