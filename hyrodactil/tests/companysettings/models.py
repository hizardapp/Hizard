from django.test import TestCase
from companysettings.models import InterviewStage
from ..factories._companysettings import InterviewStageFactory
from ..factories._companies import CompanyFactory


class InterviewStageModelTests(TestCase):

    def test_unicode(self):
        stage = InterviewStageFactory.build()
        self.assertEqual(unicode(stage), stage.name)

    def test_change_position_move_up(self):
        company = CompanyFactory()
        InterviewStageFactory(name='first', position=1, company=company)
        stage2 = InterviewStageFactory(name='second', position=2, company=company)

        stage2.change_position(-1)


        self.assertEqual(InterviewStage.objects.get(name='first').position, 2)
        self.assertEqual(InterviewStage.objects.get(name='second').position, 1)

    def test_change_position_move_down(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(name='first', position=1, company=company)
        InterviewStageFactory(name='second', position=2, company=company)

        stage1.change_position(1)


        self.assertEqual(InterviewStage.objects.get(name='first').position, 2)
        self.assertEqual(InterviewStage.objects.get(name='second').position, 1)

    def test_prepare_for_deletion(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(name='first', position=1, company=company)
        InterviewStageFactory(name='second', position=2, company=company)

        stage1.prepare_for_deletion()


        self.assertEqual(InterviewStage.objects.get(name='first').position, 1)
        self.assertEqual(InterviewStage.objects.get(name='second').position, 1)


