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

)
