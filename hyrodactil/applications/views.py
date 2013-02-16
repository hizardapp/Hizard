from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView

from braces.views import LoginRequiredMixin

from .forms import ApplicationForm
from applications.models import Application, ApplicationAnswer
from companies.models import Company
from core.views import  RestrictedListView
from jobs.models import Opening


class OpeningListView(TemplateView):
    template_name = 'applications/opening_list.html'

    def get_context_data(self, **kwargs):
        context = super(OpeningListView, self).get_context_data(**kwargs)
        company = Company.objects.get(id=self.kwargs['company_id'])
        context['company'] = company
        context['openings'] = Opening.objects.filter(company=company)
        return context


class ApplyView(TemplateView):
    template_name = 'applications/apply.html'

    def get(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404

        context = {
            'opening': opening,
            'form': ApplicationForm(opening=opening)
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404
        form = ApplicationForm(request.POST, request.FILES, opening=opening)

        if form.is_valid():
            form.save()
            return redirect('public:home')
        else:
            context = {
                'opening': opening,
                'form': form
            }
            return self.render_to_response(context)


class ApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_queryset(self):
        opening = get_object_or_404(Opening, pk=self.kwargs['opening_id'])
        return Application.objects.filter(opening=opening)


class AllApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_queryset(self):
        return Application.objects.filter(
            opening__company=self.request.user.company).order_by("opening")


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application

    def get_object(self, queryset=None):
        object = super(ApplicationDetailView, self).get_object()
        if object.opening.company == self.request.user.company:
            return object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['answers'] = ApplicationAnswer.objects.filter(application=context['application'])
        return context
