from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=50, min_length=4)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=50, min_length=3)
    last_name = forms.CharField(max_length=50, min_length=3)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    is_staff = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
                  "is_staff")



