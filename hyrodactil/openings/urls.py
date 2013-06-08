from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^$',
        views.OpeningListView.as_view(),
        name='list_openings'
    ),
    url(
        r'^new/$',
        views.OpeningCreateView.as_view(),
        name='create_opening'
    ),
    url(
        r'^(?P<pk>\d+)/edit/$',
        views.OpeningUpdateView.as_view(),
        name='update_opening'
    ),
    url(
        r'^(?P<pk>\d+)/delete/$',
        views.OpeningDeleteView.as_view(),
        name='delete_opening'
    ),
    url(
        r'^(?P<pk>\d+)/',
        views.OpeningDetailView.as_view(),
        name='detail_opening'
    ),
    url(
        r'^publish/(?P<pk>\d+)/',
        views.OpeningPublishView.as_view(),
        name='publish_opening'
    )
)
