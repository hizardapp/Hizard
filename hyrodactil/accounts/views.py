from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
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
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    """
    Logout view, only the GET method, if user is not logged in,
    redirect to the home page
    """
    def get(self, *args, **kwargs):
        msg = 'Logged out !'
        messages.info(self.request, msg)
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