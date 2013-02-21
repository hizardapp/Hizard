from django.contrib import messages
from django.http import Http404
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import BaseDeleteView


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


class RestrictedQuerysetMixin(object):
    """
    Checks if the user is allowed to do actions on this object
    """
    def get_queryset(self):
        query_set = super(RestrictedQuerysetMixin, self).get_queryset()
        query_set = query_set.filter(company=self.request.user.company)

        if len(query_set) > 0:
            return query_set
        else:
            raise Http404


class RestrictedUpdateView(RestrictedQuerysetMixin, UpdateView):
    pass


class QuickDeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


class RestrictedDeleteView(RestrictedQuerysetMixin, QuickDeleteView):
    def delete(self, request, *args, **kwargs):
        message = self.success_message
        messages.info(self.request, message)
        return super(RestrictedDeleteView, self).delete(request, *args, **kwargs)


class MessageMixin(object):
    """
    Pass a message to the template after create/update action (maybe delete)
    """
    success_message = 'Override this'

    def form_valid(self, form):
        message = self.success_message
        messages.info(self.request, message)
        return super(MessageMixin, self).form_valid(form)
