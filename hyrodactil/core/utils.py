from django.utils.translation import ugettext_lazy as _

from companysettings.models import Question, InterviewStage
from openings.models import Opening


def setup_company(company):
    website_question = Question(name=_('Website'), type='textbox')
    phone_question = Question(name=_('Phone number'), type='textbox')
    company.question_set.add(website_question)
    company.question_set.add(phone_question)

    interview_stages = [
        InterviewStage(name=_('Received')),
        InterviewStage(name=_('Phone interview')),
        InterviewStage(name=_('In-person interview')),
        InterviewStage(name=_('Rejected'), rejected=True),
        InterviewStage(name=_('Accepted'), accepted=True),
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
    ).openingquestion_set.create(
        question=phone_question,
        required=True
    )
