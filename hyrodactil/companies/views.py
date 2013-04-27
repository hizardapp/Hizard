from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from core import utils
from .forms import CompanyForm
from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('dashboard:dashboard')

    def form_valid(self, form):
        company = form.save()

        self.request.user.company = company
        self.request.user.save()

        utils.setup_company(company)

        return super(CompanyCreateView, self).form_valid(form)
