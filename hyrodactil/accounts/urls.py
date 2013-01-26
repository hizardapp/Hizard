from django.conf.urls import patterns, url

from .views import RegistrationCreateView, activate


urlpatterns = patterns('',
    url(r'register/$', RegistrationCreateView.as_view(), name='register'),
    url(r'activate/(?P<activation_key>\w+)$', activate, name='activate')
)
