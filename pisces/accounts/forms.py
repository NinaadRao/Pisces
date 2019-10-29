from django.contrib.auth import authenticate, get_user_model
from django import forms
from .models import  *


class UserUpdatePassword(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)
    confirmPassword = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserUpdatePassword, self).__init__(*args, **kwargs)
        self.fields['oldPassword'].widget.attrs.update({
            'class': 'form-control',
            "name": "Old Password"})
        self.fields['newPassword'].widget.attrs.update({
            'class': 'form-control',
            "name": "New Password"})
        self.fields['confirmPassword'].widget.attrs.update({
            'class': 'form-control',
            "name": "Confirm Password"})

    def clean(self,*args,**kwargs):
        password = self.cleaned_data.get("newPassword")
        cPassword = self.cleaned_data.get("confirmPassword")
        oldPassword = self.cleaned_data.get("oldPassword")

        if len(password)<8:
            raise forms.ValidationError('Password must be greater than 8 characters')
        if password!=cPassword:
            raise forms.ValidationError("password does not match")
        return super(UserUpdatePassword, self).clean(*args, **kwargs)


class UsersLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, )

    def __init__(self, *args, **kwargs):
        super(UsersLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name": "username"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name": "password"})

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        return super(UsersLoginForm, self).clean(*args, **keyargs)


User = get_user_model()


class UsersRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "confirm_email",
            "password",
        ]

    username = forms.CharField()
    email = forms.EmailField(label="Email")
    confirm_email = forms.EmailField(label="Confirm Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UsersRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name": "username"})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            "name": "email"})
        self.fields['confirm_email'].widget.attrs.update({
            'class': 'form-control',
            "name": "confirm_email"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name": "password"})

    def clean(self, *args, **keyargs):
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email != confirm_email:
            raise forms.ValidationError("Email must match")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email is already registered")


        # you can add more validations for password

        if len(password) < 8:
            raise forms.ValidationError("Password must be greater than 8 characters")

        return super(UsersRegisterForm, self).clean(*args, **keyargs)


