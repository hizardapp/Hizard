from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^$',
        views.AllApplicationListView.as_view(),
        name='list_all_applications'
    ),
    url(
        r'^board$',
        views.BoardView.as_view(),
        name='test_board'
    ),
    url(
        r'^(?P<opening_id>\d+)/applications$',
        views.ApplicationListView.as_view(),
        name='list_applications'
    ),
    url(
        r'^(?P<pk>\d+)$',
        views.ApplicationDetailView.as_view(),
        name='application_detail'
    ),
    url(
        r'^(?P<application_id>\d+)/create_message$',
        views.ApplicationMessageCreateView.as_view(),
        name='create_message'
    ),
)
