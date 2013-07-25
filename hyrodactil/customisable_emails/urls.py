from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^list/$',
        views.CustomisableEmailsListView.as_view(),
        name='list'
    ),
    url(
        r'^edit/(?P<pk>[\d]+)/$',
        views.CustomisableEmailsUpdateView.as_view(),
        name='edit'
    )
)
