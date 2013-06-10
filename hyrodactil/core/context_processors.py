from django.core.urlresolvers import reverse
from django.conf import settings


def opening_lists(request):
    extra_context = dict(
        PUBLIC_URL=settings.PUBLIC_URL,
        SITE_PREFIX=settings.SITE_PREFIX
    )

    if request.user.is_authenticated() and request.user.company is not None:
        extra_context['opening_list_url'] = (settings.COMPANY_URL_PREFIX
                % request.user.company.subdomain)
        if not settings.OPENING_URL_REWRITED:
            extra_context["opening_list_url"] = "%s%s" % (
                extra_context["opening_list_url"],
                reverse("public:opening-list")
            )

    return extra_context
