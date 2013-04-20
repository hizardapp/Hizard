from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'',
        include(
            'accounts.auth_urls',
            namespace='auth',
            app_name='accounts'
        )
    ),
    url(
        r'^accounts/',
        include(
            'accounts.urls',
            namespace='accounts',
            app_name='accounts'
        )
    ),
    url(
        r'^companies/',
        include(
            'companies.urls',
            namespace='companies',
            app_name='companies'
        )
    ),
    url(
        r'^settings/',
        include(
            'companysettings.urls',
            namespace='companysettings',
            app_name='companysettings'
        )
    ),
    url(
        r'^openings/',
        include(
            'openings.urls',
            namespace='openings',
            app_name='openings')
    ),
    url(
        r'^applications/',
        include(
            'applications.urls',
            namespace='applications',
            app_name='applications')
    ),
    url(
        r'^jobs/',
        include(
            'public_jobs.urls',
            namespace='public_jobs',
            app_name='public_jobs')
    ),
    url(
        r'^dashboard/',
        include(
            'dashboard.urls',
            namespace='dashboard',
            app_name='dashboard')
    ),
    url(
        r'^',
        include(
            'public.urls',
            namespace='public',
            app_name='public')
    )

)

if settings.DEBUG:
      urlpatterns += patterns('',
          (r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
     )
