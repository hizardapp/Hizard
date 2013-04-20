from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import BaseDeleteView

from braces.views import AccessMixin, redirect_to_login, PermissionDenied

from core.utils import build_host_part


class DomainLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.raise_exception:
                raise PermissionDenied # return a forbidden response
            else:
                response = redirect_to_login(request.get_full_path(),
                    self.get_login_url(), self.get_redirect_field_name())

                response["Location"] = "%s%s" % (
                        build_host_part(self.request, settings.SITE_URL),
                        response["Location"])
                return response

        return super(DomainLoginRequiredMixin, self).dispatch(
                request, *args, **kwargs)


class RestrictedListView(ListView):
    """
    Filter on object by the user's company
    """
    def get_queryset(self):
        company = self.request.user.company

        if company and company.subdomain == self.request.subdomain:
            return self.model.objects.filter(company=company)
        else:
            raise Http404


class RestrictedQuerysetMixin(object):
    """
    Checks if the user is allowed to do actions on this object
    """
    def get_queryset(self):
        query_set = super(RestrictedQuerysetMixin, self).get_queryset()
        company = self.request.user.company
        query_set = query_set.filter(company=company)

        if self.request.subdomain != company.subdomain:
            raise Http404
        else:
            return query_set


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
