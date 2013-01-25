from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm
from .models import CustomUser


class RegistrationCreateView(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    success_url = reverse_lazy('public:home')
    template_name = 'accounts/registration_form.html'
