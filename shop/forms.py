from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter User Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email Id'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Password'
        })
    )
    password2 = forms.CharField(
        label=' Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
