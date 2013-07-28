from django.utils.translation import ugettext_lazy as _

from companysettings.models import InterviewStage
from openings.models import Opening
from customisable_emails.models import EmailTemplate


def setup_company(company):

    interview_stages = [
        InterviewStage(name=_('Phone interview')),
        InterviewStage(name=_('In-person interview')),
        InterviewStage(name=_('Offer')),
        InterviewStage(name=_('Received'), tag='RECEIVED'),
        InterviewStage(name=_('Rejected'), tag='REJECTED'),
        InterviewStage(name=_('Hired'), tag='HIRED'),
    ]

    for stage in interview_stages:
        company.interviewstage_set.add(stage)

    Opening.objects.create(
        company=company,
        title=_("Professor of magic"),
        description=_("""<p>We are looking for a talented magician to join our school in London.</p>

        <p>The professor should be a master of Herbology, Potions and Time Travel. Previous experience in teaching would be an advantage.</p>

        <p>As part of our teaching team you will be able to spend 30% of your time doing research.</p>

        <p>We are a small but growing university with a bright future ahead of us, enabling hundred of students to learn about magic.</p>"""),
        country="GB",
        city="London"
    )

    EmailTemplate.objects.create(
        company=company,
        code="application_received",
        name="Application received",
        subject="Thank your for applying",
        body="""Dear {{applicant_first_name}},
Your application has successfully been received.
Best regards""",
    )

    EmailTemplate.objects.create(
        company=company,
        code="candidate_hired",
        name="Candidate hired",
        subject="Congratulations",
        body="""Dear {{applicant_first_name}},
Your application has been accepted.
Best regards""",
    )
