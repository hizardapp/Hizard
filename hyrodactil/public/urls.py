from django.conf.urls import patterns, url

from .views import HomeView, JobListView, JobList2View

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^test/(?P<company_id>\d+)/$', JobListView.as_view(), name='test'),
    url(r'^test2/(?P<company_id>\d+)/$', JobList2View.as_view(), name='test2'),
)
