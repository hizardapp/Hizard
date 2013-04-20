from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^$',
        views.DashboardView.as_view(),
        name='dashboard'
    ),
)
