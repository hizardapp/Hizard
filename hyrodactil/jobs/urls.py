from django.conf.urls import patterns, url

from .views import (
    OpeningCreateView, OpeningListView, OpeningUpdateView, ApplicationListView,
    ApplicationDetailView, apply
)

urlpatterns = patterns('',
    url(r'^$', OpeningListView.as_view(), name='list_openings'),
    url(r'new/$', OpeningCreateView.as_view(), name='create_opening'),
    url(r'(?P<pk>\d+)$', OpeningUpdateView.as_view(), name='update_opening'),

    url(r'(?P<opening_id>\d+)/applications',
        ApplicationListView.as_view(),
        name='list_applications'
    ),
    url(r'application/(?P<pk>\d+)',
        ApplicationDetailView.as_view(),
        name='application_detail'
    ),

    url(r'apply/(?P<opening_id>\d+)$', apply, name='apply'),
)
