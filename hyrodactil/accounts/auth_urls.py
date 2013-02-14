from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^login/$',
        views.LoginView.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        r'^password/change/$',
        views.PasswordChangeView.as_view(),
        name='change_password'
    ),
    url(
        r'^password/reset/$',
        views.PasswordResetView.as_view(),
        name='reset_password'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.PasswordConfirmResetView.as_view(),
        name='confirm_reset_password'
    ),
)
