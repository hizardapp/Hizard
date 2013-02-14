from django.conf.urls import patterns, url

from .views import (
    OpeningCreateView,
    OpeningRestrictedListView, OpeningUpdateView, OpeningDeleteView
)

urlpatterns = patterns('',
    url(r'^$', OpeningRestrictedListView.as_view(), name='list_openings'),
    url(r'new/$', OpeningCreateView.as_view(), name='create_opening'),
    url(r'(?P<pk>\d+)$', OpeningUpdateView.as_view(), name='update_opening'),
    url(r'(?P<pk>\d+)/delete$', OpeningDeleteView.as_view(), name='delete_opening'),
)
