from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^$',
        views.HomeView.as_view(),
        name='home'
    ),
    url(
        r'^(?P<opening_id>\d+)/apply/$',
        views.ApplyView.as_view(),
        name='apply'
    ),
    url(
        r'^(?P<opening_id>\d+)/applied/$',
        views.ApplicationConfirmationView.as_view(),
        name='confirmation'
    ),
)
