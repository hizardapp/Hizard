from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
   url(
       r'^$',
       views.ApplicationListView.as_view(),
       name='list_applications'
   ),
   url(
       r'^list/(?P<pk>\d+)/$',
       views.ApplicationListView.as_view(),
       name='list_applications_opening'
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
        r'^add/(?P<opening_id>\d+)/$',
        views.ManualApplicationView.as_view(),
        name='manual_application'
   ),
   url(
       r'^rate/(?P<application_id>\d+)/(?P<rating>-?\d+)$',
       views.RateView.as_view(),
       name='rate'
   )
)
