from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^applications$',
        views.AllApplicationListView.as_view(),
        name='list_all_applications'
    ),
    url(
        r'^(?P<opening_id>\d+)/applications$',
        views.ApplicationListView.as_view(),
        name='list_applications'
    ),
    url(
        r'^application/(?P<pk>\d+)$',
        views.ApplicationDetailView.as_view(),
        name='application_detail'
    ),
)
