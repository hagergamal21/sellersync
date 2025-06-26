from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    class RegisterForm(forms.Form):
     username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords do not match!")

        try:
            validate_password(password)  # Apply Django's password validators
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password2

