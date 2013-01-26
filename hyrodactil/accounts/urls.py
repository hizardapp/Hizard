from django.conf.urls import patterns, url

from .views import RegistrationCreateView, ActivateView


urlpatterns = patterns('',
    url(r'register/$', RegistrationCreateView.as_view(), name='register'),
    url(r'activate/(?P<activation_key>\w+)$', ActivateView.as_view(), name='activate')
)
