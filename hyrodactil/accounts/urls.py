from django.conf.urls import patterns, url

from .views import RegistrationView, ActivateView


urlpatterns = patterns('',
    url(r'register/$', RegistrationView.as_view(), name='register'),
    url(r'activate/(?P<activation_key>\w+)$', ActivateView.as_view(), name='activate')
)
