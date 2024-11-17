from allauth.account.forms import LoginForm, SignupForm, SetPasswordField, PasswordField
from django import forms
from turnstile.fields import TurnstileField
from core.widgets import ShoelaceInput, ShoelaceCheckBox

class UserCoreLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = ShoelaceInput(attrs={'placeholder': 'Username', 'label': 'Username','autocomplete': 'username', 'required': True, 'clearable': True})
        self.fields['password'].widget = ShoelaceInput(attrs={'placeholder': 'Password', 'label': 'Password','autocomplete': 'password', 'type': 'password', 'required': True, 'password-toggle': True, 'clearable': True})
        self.fields['remember'].widget = ShoelaceCheckBox(attrs={'label': 'Remember Me'})

    turnstile = TurnstileField(label=False)


class UserCoreSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = ShoelaceInput(attrs={'placeholder': 'Password', 'label': 'Password','autocomplete': 'new-password', 'type': 'password', 'required': True, 'password-toggle': True, 'clearable': True})
        self.fields['password2'].widget = ShoelaceInput(attrs={'placeholder': 'Confirm Password', 'label': 'Confirm Password','autocomplete': 'new-password', 'type': 'password', 'required': True, 'password-toggle': True, 'clearable': True})

    username = forms.CharField(widget=ShoelaceInput(attrs={'placeholder': 'Username', 'label': 'Username','autocomplete': 'name', 'required': True, 'clearable': True}))
    email = forms.EmailField(widget=ShoelaceInput(attrs={'placeholder': 'Email', 'label': 'Email','autocomplete': 'email', 'type': 'email', 'required': True, 'clearable': True}))
    password1 = SetPasswordField()
    password2 = PasswordField()
    turnstile = TurnstileField(label=False)
    field_order = ['username', 'email', 'password1', 'password2', 'turnstile']