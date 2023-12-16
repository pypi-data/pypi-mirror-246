from django import forms
from utilities.forms import TailwindMixin


class DemoLoginForm(TailwindMixin, forms.Form):
    username = forms.CharField(
        required=False,
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
    )
