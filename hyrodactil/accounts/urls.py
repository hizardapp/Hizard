from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^register/$',
        views.RegistrationView.as_view(),
        name='register'
    ),
    url(
        r'^confirmation/$',
        views.RegistrationConfirmationView.as_view(),
        name='register_confirmation'
    ),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        views.ActivateView.as_view(),
        name='activate'
    ),
    url(
        r'^toggle_status/(?P<user_pk>\w+)/$',
        views.ToggleStatusView.as_view(),
        name='toggle_status'
    ),
    url(
        r'^change_details/$',
        views.ChangeDetailsView.as_view(),
        name='change_details'
    )
)
