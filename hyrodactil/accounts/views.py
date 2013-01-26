from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView, View

from .forms import UserCreationForm
from .models import CustomUser


class RegistrationCreateView(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    success_url = reverse_lazy('public:home')
    template_name = 'accounts/registration_form.html'


def activate(request, activation_key):
    raise Http404


class LoginFormView(FormView):
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

        return super(LoginFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    """
    Logout view, only the GET method, if user is not logged in,
    redirect to the home page
    """
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            msg = 'Logged out !'
            messages.info(self.request, msg)
            logout(self.request)
        return HttpResponseRedirect(reverse('public:home'))
