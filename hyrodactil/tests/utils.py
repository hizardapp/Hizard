from django.conf import settings


def subdomain_get(app, view_name, user=None, status=None):
    response = app.get(
        view_name,
        user=user,
        status=status,
        headers=dict(Host=settings.APP_SITE_DOMAIN)
    )

    if response.status_code in [301, 302]:
        return response.follow()

    return response

def subdomain_post_ajax(app, view_name, data, user=None, status=None):
    response = app.post(
        view_name,
        data,
        user=user,
        status=status,
        headers=dict(Host=settings.APP_SITE_DOMAIN),
        extra_environ=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    )

    if response.status_code in [301, 302]:
        return response.follow()

    return response

def career_site_get(app, view_name, company_name):
    response = app.get(
        view_name,
        headers=dict(Host="%s.%s" % (company_name, settings.PUBLIC_DOMAIN))
    )

    if response.status_code in [301, 302]:
        return response.follow()

    return response