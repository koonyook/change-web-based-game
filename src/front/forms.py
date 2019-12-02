from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email")
    latitude = forms.IntegerField()
    longitude = forms.IntegerField()
    
