from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from .forms import CompanyForm
from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('jobs:list_openings')

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner = self.request.user
        company.save()
        return super(CompanyCreateView, self).form_valid(form)
