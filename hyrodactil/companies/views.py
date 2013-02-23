from django.core.urlresolvers import reverse
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from core.utils import build_subdomain_url
from .forms import CompanyForm
from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm

    def get_success_url(self):
        return build_subdomain_url(self.request,
            reverse('openings:list_openings'))

    def form_valid(self, form):
        company = form.save(commit=False)
        company.save()

        self.request.user.company = company
        self.request.user.save()

        return super(CompanyCreateView, self).form_valid(form)
