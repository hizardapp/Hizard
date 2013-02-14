from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^$',
        views.OpeningRestrictedListView.as_view(),
        name='list_openings'
    ),
    url(
        r'^new/$',
        views.OpeningCreateView.as_view(),
        name='create_opening'
    ),
    url(
        r'^(?P<pk>\d+)$',
        views.OpeningUpdateView.as_view(),
        name='update_opening'
    ),
    url(
        r'^(?P<pk>\d+)/delete$',
        views.OpeningDeleteView.as_view(),
        name='delete_opening'
    ),
)
