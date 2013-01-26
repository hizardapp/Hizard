from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """
    Form used by the admin and the site to add a user
    """
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = _('Passwords don\'t match')
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        """
        Save the user using the manager to make sure it creates the
        activation token and sens the activation email
        """
        email = self.cleaned_data["password1"]
        password = self.cleaned_data["password1"]

        if commit:
            user = CustomUser.objects.create_user(email, password, False)
            return user