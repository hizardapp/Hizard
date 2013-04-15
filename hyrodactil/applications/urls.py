from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
   url(
       r'^$',
       views.BoardView.as_view(),
       name='board_applications'
   ),
    url(
        r'^list/$',
        views.AllApplicationListView.as_view(),
        name='list_all_applications'
    ),
    url(
        r'^update_positions/$',
        views.UpdatePositionsAjaxView.as_view(),
        name='update_positions'
    ),
    url(
        r'^(?P<opening_id>\d+)/list/$',
        views.ApplicationListView.as_view(),
        name='list_applications'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        views.ApplicationDetailView.as_view(),
        name='application_detail'
    ),
    url(
        r'^(?P<application_id>\d+)/create_message/$',
        views.ApplicationMessageCreateView.as_view(),
        name='create_message'
    ),
    url(
        r'^(?P<opening_id>\d+)/add_application/$',
        views.ManualApplicationView.as_view(),
        name='manual_application'
    )
)
