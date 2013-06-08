from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser


class ImageWidget(forms.FileInput):
    template = '%(input)s<br />%(image)s'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        input_html = super(forms.FileInput, self).render(name, value, attrs)
        if hasattr(value, 'width') and hasattr(value, 'height'):
            image_html = '<img src="%s" width="%d" height="%d">' % (value.url, self.width, self.height)
            output = self.template % {'input': input_html,
                                      'image': image_html}
        else:
            output = input_html
        return mark_safe(output)


class UserCreationForm(forms.ModelForm):
    """
    Form used by the admin and the site to add a user
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'short_password': _(
            "Password is too short. Should be at least %d characters."
            % settings.MIN_PASSWORD_LENGTH
        )
    }

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ('name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch']
            )

        # No insecure passwords !
        if len(password2) < settings.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(self.error_messages['short_password'])

        return password2

    def save(self, commit=True):
        """
        Save the user using the manager to make sure it creates the
        activation token and sens the activation email
        """
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        name = self.cleaned_data['name']

        if commit:
            user = CustomUser.objects.create_user(
                email,
                name,
                password=password,
                active=False,
                is_company_admin=True
            )
            return user


class InvitedRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = tuple()

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance


class MinLengthSetPasswordForm(auth_forms.SetPasswordForm):
    """
    Extends the basic reset password form and adds the restriction on
    password length.
    """

    error_messages = dict(auth_forms.SetPasswordForm.error_messages, **{
        'short_password': _(
            "Password is too short. Should be at least %d characters."
            % settings.MIN_PASSWORD_LENGTH
        )
    })

    def clean_new_password2(self):
        password2 = super(MinLengthSetPasswordForm, self).clean_new_password2()

        # No insecure passwords !
        if len(password2) < settings.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(self.error_messages['short_password'])


class MinLengthChangePasswordForm(auth_forms.PasswordChangeForm):
    """
    Extends the basic reset password form and adds the restriction on
    password length.
    """
    error_messages = dict(auth_forms.PasswordChangeForm.error_messages, **{
        'short_password': _(
            "Password is too short. Should be at least %d characters."
            % settings.MIN_PASSWORD_LENGTH
        )
    })

    def clean_new_password2(self):
        password2 = super(MinLengthChangePasswordForm, self).clean_new_password2()

        # No insecure passwords !
        if len(password2) < settings.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(self.error_messages['short_password'])


class ChangeDetailsForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'avatar')
        model = CustomUser


    def __init__(self, *args, **kwargs):
        super(ChangeDetailsForm, self).__init__(*args, **kwargs)

        # change a widget attribute:
        self.fields['avatar'].widget = ImageWidget()
