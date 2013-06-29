from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
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
        views.InterviewStageCreateUpdateView.as_view(),
        name='ajax_stage'
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
        views.InviteUserCreateView.as_view(),
        name='list_users'
    ),
    url(
        r'^information/$',
        views.UpdateCompanyInformationView.as_view(),
        name='update_information'
    ),

)
