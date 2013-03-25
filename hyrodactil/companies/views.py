from django.core.urlresolvers import reverse
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from core import utils
from .forms import CompanyForm
from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm

    def get_success_url(self):
        return utils.build_subdomain_url(
            self.request,
            reverse('openings:list_openings')
        )

    def form_valid(self, form):
        company = form.save(commit=False)
        company.save()

        self.request.user.company = company
        self.request.user.save()

        utils.setup_company(company)

        return super(CompanyCreateView, self).form_valid(form)
