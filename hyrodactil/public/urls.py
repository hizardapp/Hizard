from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^landing_page/$',
        views.LandingPageView.as_view(),
        name='landing-page'
    ),
    url(
        r'^opening_list/$',
        views.OpeningList.as_view(),
        name='opening-list'
    ),
    url(
        r'^(?P<opening_id>\d+)/apply/$',
        views.ApplyView.as_view(),
        name='apply'
    ),
    url(
        r'^(?P<opening_id>\d+)/applied/$',
        views.ApplicationConfirmationView.as_view(),
        name='confirmation'
    ),
    url(
        r'^add_interest/$',
        views.add_interest,
        name='add-interest'
    ),
)
