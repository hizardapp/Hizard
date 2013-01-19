from django.conf.urls import patterns, url

from .views import CompanyCreateView, DepartmentCreateView,DepartmentListView

urlpatterns = patterns('',
    url(r'create/$', CompanyCreateView.as_view(), name='create'),

    url(r'departments/$', DepartmentListView.as_view(),
        name='list_departments'),
    url(r'department$', DepartmentCreateView.as_view(),
        name='create_department'),
)
