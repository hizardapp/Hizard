from django.conf.urls import patterns, url

from .views import HomeView, JobListView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^test/(?P<company_id>\d+)/$', JobListView.as_view(), name='test'),
)
