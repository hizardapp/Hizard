from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
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
