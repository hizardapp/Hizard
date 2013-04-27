from django.contrib import messages
from django.views.generic.edit import BaseDeleteView


class SubdomainMixin(object):
    def dispatch(self, *args, **kwargs):
        domain_parts = self.request.get_host().split('.')
        if len(domain_parts) > 2:
            self.request.subdomain = domain_parts[0]
        else:
            self.request.subdomain = None

        return super(SubdomainMixin, self).dispatch(*args, **kwargs)


class QuickDeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        message = self.success_message
        messages.info(self.request, message)
        return super(QuickDeleteView, self).delete(request, *args, **kwargs)


class MessageMixin(object):
    """
    Pass a message to the template after create/update action (maybe delete)
    """
    success_message = 'Override this'

    def form_valid(self, form):
        message = self.success_message
        messages.info(self.request, message)
        return super(MessageMixin, self).form_valid(form)
