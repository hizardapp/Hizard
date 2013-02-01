from django.contrib import messages
from django.http import Http404
from django.views.generic import ListView, UpdateView, DetailView


class RestrictedListView(ListView):
    """
    Filter on object by the user's company
    """
    def get_queryset(self):
        company = self.request.user.company

        if company:
            return self.model.objects.filter(company=company)
        else:
            raise Http404


class RestrictedUpdateView(UpdateView):
    """
    Checks if the user is allowed to do actions on this object
    """
    def get_queryset(self):
        query_set = super(RestrictedUpdateView, self).get_queryset()
        query_set = query_set.filter(company=self.request.user.company)

        if len(query_set) > 0:
            return query_set
        else:
            raise Http404


class RestrictedDetailView(DetailView):
    """
    Check if the user is allowed to view the details of this object
    """
    model = None
    # In case the model in the detail view has its ownership data from a
    # related object
    restricted_by_model = None

    def get_queryset(self):
        query_set = super(RestrictedDetailView, self).get_queryset()

        if self.restricted_by_model:
            # The model is related to another model which has a company field
            pass
        else:
            # The model has a company field
            query_set = query_set.filter(company=self.request.user.company)

        if len(query_set) > 0:
            return query_set
        else:
            raise Http404


class MessageMixin(object):
    """
    Pass a message to the template after create/update action (maybe delete)
    """
    success_message = 'Override this'

    def form_valid(self, form):
        message = self.success_message
        messages.info(self.request, message)
        return super(MessageMixin, self).form_valid(form)