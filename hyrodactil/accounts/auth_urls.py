from django.conf.urls import patterns, url

from django.contrib.auth import views as auth_views

from .views import LoginView, LogoutView, PasswordChangeView


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

    url(r'^password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
)
