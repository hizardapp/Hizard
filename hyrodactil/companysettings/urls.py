from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^departments/$',
        views.DepartmentRestrictedListView.as_view(),
        name='list_departments'
    ),
    url(
        r'^department$',
        views.DepartmentCreateView.as_view(),
        name='create_department'
    ),
    url(
        r'^department/(?P<pk>\d+)$',
        views.DepartmentUpdateView.as_view(),
        name='update_department'
    ),
    url(
        r'^department/(?P<pk>\d+)/delete$',
        views.DepartmentDeleteView.as_view(),
        name='delete_department'
    ),

    url(
        r'^questions/$',
        views.QuestionRestrictedListView.as_view(),
        name='list_questions'
    ),
    url(
        r'^question$',
        views.QuestionCreateView.as_view(),
        name='create_question'
    ),
    url(
        r'^question/(?P<pk>\d+)$',
        views.QuestionUpdateView.as_view(),
        name='update_question'
    ),
    url(
        r'^question/(?P<pk>\d+)/delete$',
        views.QuestionDeleteView.as_view(),
        name='delete_question'
    ),

    url(
        r'^stages/$',
        views.InterviewStageRestrictedListView.as_view(),
        name='list_stages'
    ),
    url(
        r'^stage$',
        views.InterviewStageCreateView.as_view(),
        name='create_stage'
    ),
    url(
        r'^stage/(?P<pk>\d+)$',
        views.InterviewStageUpdateView.as_view(),
        name='update_stage'
    ),
    url(
        r'^stage/(?P<pk>\d+)/delete$',
        views.InterviewStageDeleteView.as_view(),
        name='delete_stage'
    ),

    url(
        r'^users/$',
        views.UsersListView.as_view(),
        name='list_users'
    ),


    url(
        r'^$',
        views.SettingsHomeView.as_view(),
        name='settings_home'
    ),

)
