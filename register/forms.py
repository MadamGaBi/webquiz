from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _


class UserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=50,
                               min_length=4)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=50,
                                 min_length=3)
    last_name = forms.CharField(max_length=50,
                                min_length=3)
    password1 = forms.CharField(max_length=50,
                                label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50,
                                label=("Password confirmation"),
                                widget=forms.PasswordInput)
                                # help_text=_("Enter the same password as above, for verification."))
    is_staff = forms.BooleanField(required=False,
                                  label=(""),
                                  help_text=_("Tick if you are a Tutor! Be honest!"))

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
                  "is_staff")



