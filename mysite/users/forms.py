from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model() #use the custom user model instead

class CreateUserForm(UserCreationForm):
    #form used inside the register view
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Change place holders of the registration form
        self.fields['username'].widget.attrs.update({'placeholder': ('Username')})
        self.fields['email'].widget.attrs.update({'placeholder': ('Email')})
        self.fields['password1'].widget.attrs.update({'placeholder': ('Password')})
        self.fields['password2'].widget.attrs.update({'placeholder': ('Confirm Password')})
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUserForm(AuthenticationForm):
    pass

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


