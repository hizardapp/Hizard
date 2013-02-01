from braces.views import LoginRequiredMixin

from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView, View

from .forms import UserCreationForm
from .models import CustomUser


class RegistrationView(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    success_url = reverse_lazy('public:home')
    template_name = 'accounts/registration_form.html'


class ActivateView(View):
    """
    Called with an activation key as a parameter
    """
    def get(self, *args, **kwargs):
        activation_key = kwargs['activation_key']
        activated = CustomUser.objects.activate_user(activation_key)

        if activated:
            return HttpResponseRedirect(reverse('public:home'))
        else:
            raise Http404


class LoginView(FormView):
    """
    Login view, not using auth view in case we want to override some things
    """
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('public:home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('public:home'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.company is None:
            self.success_url = reverse('companies:create')
        return super(LoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    """
    Logout view, only the GET method, if user is not logged in,
    redirect to the home page
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('public:home'))


class PasswordChangeView(LoginRequiredMixin, FormView):
    """
    Change password view, only for logged in users
    """
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('public:home')

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
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('public:home')

    def form_valid(self, form):
        """
        Email is valid, preparing data to be sent to the save form method
        """
        opts = {
            'use_https': self.request.is_secure(),
            'from_email': 'Hyrodactil',
            'subject_template_name': 'accounts/password_reset_subject.txt',
            'email_template_name': 'accounts/password_reset_email.html',
            'request': self.request,
        }
        form.save(**opts)
        return super(PasswordResetView, self).form_valid(form)


class PasswordConfirmResetView(FormView):
    form_class = SetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('public:home')

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
