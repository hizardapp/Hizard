from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from .forms import OpeningForm
from .models import Opening, OpeningQuestion
from core.views import MessageMixin, RestrictedListView, RestrictedUpdateView
from core.views import RestrictedDeleteView
from companysettings.models import Question


class OpeningRestrictedListView(LoginRequiredMixin, RestrictedListView):
    model = Opening


class OpeningCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Opening
    form_class = OpeningForm
    action = 'created'
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening created.')

    def get_form(self, form_class):
        return form_class(self.request.user.company, **self.get_form_kwargs())


class OpeningUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = Opening
    form_class = OpeningForm
    action = 'updated'
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening updated.')

    def get_form(self, form_class):
        opening_questions = OpeningQuestion.objects.filter(opening=self.object)
        return form_class(
            self.request.user.company, opening_questions, **self.get_form_kwargs()
        )

    def _form_valid(self, form):
        instance = form.save()
        questions = self.request.POST.getlist('questions')
        questions_required = self.request.POST.getlist('questions_required')
        OpeningQuestion.objects.filter(opening=instance).delete()

        for id in questions:
            question = Question.objects.filter(id=id, company=self.request.user.company)[0]
            if question:
                opening_question = OpeningQuestion(
                    opening=instance, question=question
                )
                if id in questions_required:
                    opening_question.required = True
                opening_question.save()
        return HttpResponseRedirect(self.get_success_url())


class OpeningDeleteView(LoginRequiredMixin, RestrictedDeleteView):
    model = Opening
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening deleted.')
