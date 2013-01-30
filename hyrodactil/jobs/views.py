from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView


from .forms import OpeningForm
from .models import Application, ApplicationAnswer, Opening
from companies.models import Company
from core.views import GetCompanyObjectsMixin


class OpeningListView(GetCompanyObjectsMixin, ListView):
    model = Opening


class OpeningActionMixin(object):
    def form_valid(self, form):
        msg = 'Opening {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(OpeningActionMixin, self).form_valid(form)


class OpeningCreateView(OpeningActionMixin, CreateView):
    model = Opening
    form_class = OpeningForm
    action = 'created'
    success_url = reverse_lazy('jobs:list_openings')

    def form_valid(self, form):
        opening = form.save(commit=False)
        opening.company = Company.objects.get(id=self.request.user.company.id)
        opening.save()
        form.save_m2m()
        return super(OpeningCreateView, self).form_valid(form)


class OpeningUpdateView(OpeningActionMixin, UpdateView):
    model = Opening
    form_class = OpeningForm
    action = 'updated'
    success_url = reverse_lazy('jobs:list_openings')


class ApplicationListView(ListView):
    def get_queryset(self):
        opening = get_object_or_404(Opening, pk=self.kwargs['opening_id'])
        return Application.objects.filter(opening=opening)


class ApplicationDetailView(DetailView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['answers'] = ApplicationAnswer.objects.filter(application=context['application'])
        return context

@csrf_exempt
def apply(request, opening_id):
    try:
        opening = Opening.objects.get(id=opening_id)
    except:
        opening = None

    if not opening:
        data = 'fail'
        return HttpResponse(data, mimetype='application/json')

    data = request.POST.dict()

    application = Application(opening=opening)
    application.first_name = data['first-name']
    application.last_name = data['last-name']
    application.save()

    del(data['first-name'])
    del(data['last-name'])
    questions = opening.questions.all()

    for key in data.keys():
        application_answer = ApplicationAnswer()

        # Not very beautiful but works, for now
        question = [question for question in questions if question.name == key]
        # If no questions matches, skip this one
        if len(question) == 0:
            continue

        application_answer.question = question[0]

        application_answer.application = application
        application_answer.answer = data[key]
        application_answer.save()

    data = 'applied'
    return HttpResponse(data, mimetype='application/json')
