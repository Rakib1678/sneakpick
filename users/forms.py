from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignupForm(UserCreationForm):
    """Modified Signup Form based off of built-in forms.
    Will take in email from UserProfile class during signup.

    Args:
        UserCreationForm (UserCreationForm): Extension of built-in
        UserCreationForm.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
