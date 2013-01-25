from django.conf.urls import patterns, url

from .views import RegistrationCreateView


urlpatterns = patterns('',
    url(r'register/$', RegistrationCreateView.as_view(), name='register')
)
