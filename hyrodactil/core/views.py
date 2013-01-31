from django.http import Http404


class ListCompanyObjectsMixin(object):
    """
    Filter on object by the user's company
    """
    def get_queryset(self):
        company = self.request.user.company

        if company:
            return self.model.objects.filter(company=company)
        else:
            raise Http404



class UserAllowedActionMixin(object):
    """
    Checks if the user is allowed to do actions on this object
    """
    def get_queryset(self):
        query_set = super(UserAllowedActionMixin, self).get_queryset()
        query_set = query_set.filter(company=self.request.user.company)

        if len(query_set) > 0:
            return query_set
        else:
            raise Http404
