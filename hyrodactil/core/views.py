from django.http import Http404


class GetCompanyObjectsMixin(object):
    """
    Filter on object by the user's company
    """
    def get_queryset(self):
        company = self.request.user.company

        if company:
            return self.model.objects.filter(company=company)
        else:
            raise Http404
