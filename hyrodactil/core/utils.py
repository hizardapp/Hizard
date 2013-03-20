from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from companysettings.models import Question, InterviewStage


def build_subdomain_url(request, url):
    scheme = "https" if request.is_secure() else "http"
    server_port = int(request.environ['SERVER_PORT'])
    if server_port not in (80, 443):
        host_part = "%s://%s.%s:%s" % (
            scheme,
            request.user.company.subdomain,
            settings.SITE_URL,
            server_port)
    else:
        host_part = "%s://%s.%s" % (
            scheme,
            request.user.company.subdomain,
            settings.SITE_URL)

    return "%s%s" % (host_part, url)


def setup_company(company):
    questions = [
        Question(
            name=_('Website'), type='textbox', is_default=True,
            is_required=True
        ),
        Question(
            name=_('Phone number'), type='textbox', is_default=True,
            is_required=True
        )
    ]

    for question in questions:
        company.question_set.add(question)

    interview_stages = [
        InterviewStage(name=_('Received')),
        InterviewStage(name=_('Phone interview')),
        InterviewStage(name=_('In-person interview')),
        InterviewStage(name=_('Rejected'))
    ]

    for stage in interview_stages:
        company.interviewstage_set.add(stage)

    company.save()
