from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(
        r'^companies/',
        include(
            'hyrodactil.hyrodactil.companies.urls',
            namespace='companies',
            app_name='companies'
        )
    ),

)
