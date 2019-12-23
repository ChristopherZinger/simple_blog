from django import forms
from accounts.models import User, UserInfo
from django.forms import TextInput,EmailInput,PasswordInput

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'password': PasswordInput(attrs={'placeholder': 'Password'}),
            }

class UserInfoForm(forms.ModelForm):
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    class Meta:
        model = UserInfo
        fields = ['first_name','last_name']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name'}),
            }


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    class Meta:
        fields = ['email',]


class UserUpdateForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': '* Current Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password'}), required=False)
    repeat_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat New Password'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(
    attrs={'placeholder':'* Email'}))

    class Meta:
        fields = ['email', 'new_password', 'repeat_password', 'current_password']
