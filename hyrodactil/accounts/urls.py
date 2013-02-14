from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^register/$',
        views.RegistrationView.as_view(),
        name='register'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)$',
        views.ActivateView.as_view(),
        name='activate'
    )
)
