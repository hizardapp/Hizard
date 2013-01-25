from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
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
        r'^jobs/',
        include(
            'jobs.urls',
            namespace='jobs',
            app_name='jobs')
    ),
    url(
        r'^',
        include(
            'public.urls',
            namespace='public',
            app_name='public')
    )

)
