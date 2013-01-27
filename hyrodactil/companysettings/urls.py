from django.conf.urls import patterns, url

from .views import (
    DepartmentCreateView, DepartmentListView, DepartmentUpdateView,
    QuestionListView, QuestionCreateView, QuestionUpdateView
)

urlpatterns = patterns('',
    url(r'departments/$', DepartmentListView.as_view(),
        name='list_departments'),
    url(r'department$', DepartmentCreateView.as_view(),
        name='create_department'),
    url(r'department/(?P<pk>\d+)$', DepartmentUpdateView.as_view(),
        name='update_department'),

    url(r'questions/$', QuestionListView.as_view(),
        name='list_questions'),
    url(r'question$', QuestionCreateView.as_view(),
        name='create_question'),
    url(r'question/(?P<pk>\d+)$', QuestionUpdateView.as_view(),
        name='update_question'),
)
