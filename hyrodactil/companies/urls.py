from django.conf.urls import patterns, url

from .views import CompanyCreateView

urlpatterns = patterns('',
    url(r'create/$', CompanyCreateView.as_view(), name='create'),
)
