from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(
        r'^departments/$',
        views.DepartmentListView.as_view(),
        name='list_departments'
    ),
    url(
        r'^department/$',
        views.DepartmentCreateUpdateView.as_view(),
        name='ajax_department'
    ),
    url(
        r'^department/(?P<pk>\d+)/delete$',
        views.DepartmentDeleteView.as_view(),
        name='delete_department'
    ),
    url(
        r'^questions/$',
        views.QuestionListView.as_view(),
        name='list_questions'
    ),
    url(
        r'^question/$',
        views.QuestionCreateUpdateView.as_view(),
        name='ajax_question'
    ),
    url(
        r'^question/(?P<pk>\d+)/delete/$',
        views.QuestionDeleteView.as_view(),
        name='delete_question'
    ),

    url(
        r'^stages/$',
        views.InterviewStageListView.as_view(),
        name='list_stages'
    ),
    url(
        r'^stage/$',
        views.InterviewStageCreateView.as_view(),
        name='create_stage'
    ),
    url(
        r'^stage/(?P<pk>\d+)/$',
        views.InterviewStageUpdateView.as_view(),
        name='update_stage'
    ),
    url(
        r'^stage/(?P<pk>\d+)/delete/$',
        views.InterviewStageDeleteView.as_view(),
        name='delete_stage'
    ),
    url(
        r'^stage/(?P<pk>\d+)/reorder/(?P<direction>[a-z]+)/$',
        views.InterviewStageReorderView.as_view(),
        name='reorder_stage'
    ),

    url(
        r'^users/$',
        views.UsersListView.as_view(),
        name='list_users'
    ),
    url(
        r'^users/invite/$',
        views.InviteUserCreateView.as_view(),
        name='invite_user'
    ),
    url(
        r'^information/$',
        views.UpdateCompanyInformationView.as_view(),
        name='update_information'
    ),

    url(
        r'^$',
        views.SettingsHomeView.as_view(),
        name='settings_home'
    ),

)
