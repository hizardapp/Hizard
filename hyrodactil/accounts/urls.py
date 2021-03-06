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
        r'^promote/(?P<user_pk>\w+)/$',
        views.PromoteView.as_view(),
        name='promote'
    ),
    url(
        r'^delete/(?P<user_pk>\w+)/$',
        views.DeleteView.as_view(),
        name='delete'
    ),
    url(
        r'^details/$',
        views.ChangeDetailsView.as_view(),
        name='change_details'
    )
)
