from django.conf.urls import patterns, url

from .views import (
    DepartmentCreateView, DepartmentRestrictedListView, DepartmentUpdateView,
    QuestionRestrictedListView, QuestionCreateView, QuestionUpdateView,
    InterviewStageRestrictedListView, InterviewStageCreateView, InterviewStageUpdateView,
    DepartmentDeleteView
)

urlpatterns = patterns('',
    url(r'departments/$', DepartmentRestrictedListView.as_view(),
        name='list_departments'),
    url(r'department$', DepartmentCreateView.as_view(),
        name='create_department'),
    url(r'department/(?P<pk>\d+)$', DepartmentUpdateView.as_view(),
        name='update_department'),
    url(r'department/(?P<pk>\d+)/delete$', DepartmentDeleteView.as_view(),
        name='delete_department'),

    url(r'questions/$', QuestionRestrictedListView.as_view(),
        name='list_questions'),
    url(r'question$', QuestionCreateView.as_view(),
        name='create_question'),
    url(r'question/(?P<pk>\d+)$', QuestionUpdateView.as_view(),
        name='update_question'),

    url(r'stages/$', InterviewStageRestrictedListView.as_view(),
        name='list_stages'),
    url(r'stage$', InterviewStageCreateView.as_view(),
        name='create_stage'),
    url(r'stage/(?P<pk>\d+)$', InterviewStageUpdateView.as_view(),
        name='update_stage'),
)
