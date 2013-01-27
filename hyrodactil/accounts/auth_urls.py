from django.conf.urls import patterns, url

from .views import LoginView, LogoutView, PasswordChangeView, PasswordConfirmResetView, PasswordResetView


urlpatterns = patterns('',
    url(
        r'^login/$',
        LoginView.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='logout'
    ),
    url(
        r'^password/change/$',
        PasswordChangeView.as_view(),
        name='change_password'
    ),
    url(
        r'^password/reset/$',
        PasswordResetView.as_view(),
        name='reset_password'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordConfirmResetView.as_view(),
        name='confirm_reset_password'
    ),
)
