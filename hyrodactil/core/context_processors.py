from django.core.urlresolvers import reverse
from django.conf import settings


def opening_lists(request):
    extra_context = dict(
        PUBLIC_URL=settings.PUBLIC_URL,
        APP_SITE_URL=settings.APP_SITE_URL
    )

    if request.user.is_authenticated() and request.user.company is not None:
        extra_context['opening_list_url'] = "http://%s.%s" % (
            request.user.company.subdomain, settings.PUBLIC_DOMAIN
        )
        if not settings.OPENING_URL_REWRITED:
            extra_context["opening_list_url"] = "%s%s" % (
                extra_context["opening_list_url"],
                reverse("public:opening-list")
            )

    return extra_context
