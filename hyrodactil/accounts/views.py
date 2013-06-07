from braces.views import LoginRequiredMixin

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView, View, TemplateView
from django.views.generic import UpdateView

from core.views import MessageMixin
from .forms import UserCreationForm, MinLengthSetPasswordForm, ChangeDetailsForm
from .forms import MinLengthChangePasswordForm, InvitedRegistrationForm
from .models import CustomUser


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:register_confirmation')
    template_name = 'accounts/registration_form.html'


class RegistrationConfirmationView(TemplateView):
    template_name = 'accounts/registration_confirmation.html'


class ActivateView(FormView):
    form_class = InvitedRegistrationForm
    template_name = "accounts/activation_form.html"

    def dispatch(self, *args, **kwargs):
        self.activation_key = kwargs['activation_key']
        self.user = get_object_or_404(
            CustomUser,
            activation_key=self.activation_key
        )
        return super(ActivateView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        # if has a company show the changepassword form
        if self.user.company:
            return super(ActivateView, self).get(*args, **kwargs)
        else:
            user = CustomUser.objects.activate_user(self.activation_key)
            if user:
                self.request.session['from_activation'] = True
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                raise Http404

    def get_form_kwargs(self):
        kwargs = super(ActivateView, self).get_form_kwargs()
        kwargs['instance'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()

        user = CustomUser.objects.activate_user(self.activation_key)
        if user:
            return HttpResponseRedirect(reverse("dashboard:dashboard"))
        else:
            raise Http404


class LoginView(FormView):
    """
    Login view, not using auth view in case we want to override some things
    """
    form_class = auth_forms.AuthenticationForm
    template_name = 'accounts/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.request.session.get('from_activation', False):
            context['from_activation'] = True
            del self.request.session['from_activation']
        return context

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        if self.request.user.company is None:
            return reverse('companies:create')
        else:
            return reverse("dashboard:dashboard")


class LogoutView(LoginRequiredMixin, View):
    """
    Logout view, only the GET method, if user is not logged in,
    redirect to the login page
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse("auth:login"))


class PasswordChangeView(LoginRequiredMixin, FormView):
    """
    Change password view, only for logged in users
    """
    form_class = MinLengthChangePasswordForm
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('auth:login')

    def get_form_kwargs(self):
        """
        The password change form takes the user in the constructor
        """
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)


class PasswordResetView(FormView):
    """
    View with a form containing only an email field to which send the reset
    email
    """
    form_class = auth_forms.PasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        """
        Email is valid, preparing data to be sent to the save form method
        """
        opts = {
            'use_https': self.request.is_secure(),
            'from_email': 'Hizard',
            'subject_template_name': 'accounts/password_reset_subject.txt',
            'email_template_name': 'accounts/password_reset_email.html',
            'request': self.request,
        }
        form.save(**opts)
        return super(PasswordResetView, self).form_valid(form)


class PasswordConfirmResetView(FormView):
    form_class = MinLengthSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('auth:login')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_link(kwargs['uidb36'], kwargs['token']):
            return self.render_to_response(self.get_context_data(form=None))
        return super(PasswordConfirmResetView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        The password change form takes the user in the constructor
        """
        kwargs = super(PasswordConfirmResetView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        """
        We display a special message if the link is not a valid one
        """
        kwargs['valid_link'] = self.valid_link
        return super(PasswordConfirmResetView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return super(PasswordConfirmResetView, self).form_valid(form)

    def check_link(self, uidb36, token):
        """
        Check if the link that the person is accessing the page from is a
        valid one
        """
        try:
            uid_int = base36_to_int(uidb36)
            self.user = CustomUser.objects.get(id=uid_int)
        except (ValueError, OverflowError, CustomUser.DoesNotExist):
            self.user = None

        check_token = default_token_generator.check_token(self.user, token)
        self.valid_link = bool(self.user is not None and check_token)
        return self.valid_link


class ToggleStatusView(View):
    def get(self, request, user_pk):
        user = get_object_or_404(CustomUser, pk=user_pk)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, _('Changed user status.'))
        return HttpResponseRedirect(reverse("companysettings:list_users"))


class ChangeDetailsView(LoginRequiredMixin, MessageMixin, UpdateView):
    form_class = ChangeDetailsForm
    model = CustomUser
    success_message = _("Personal details successfuly updated")
    template_name = 'accounts/change_details_form.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_object(self):
        return self.request.user
