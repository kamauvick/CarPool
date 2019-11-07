from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ('first_name', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = UserChangeForm.Meta.fields
