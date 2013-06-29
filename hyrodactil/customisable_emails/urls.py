from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^list/$',
        views.CustomisableEmailsListView.as_view(),
        name='list'
    ),
)
