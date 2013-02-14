from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^(?P<company_id>\d+)$',
        views.OpeningListView.as_view(),
        name='list_openings'
    ),
    url(
        r'^(?P<opening_id>\d+)/apply/$',
        views.ApplyView.as_view(),
        name='apply'
    ),


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
