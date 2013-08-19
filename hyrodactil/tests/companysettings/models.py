from django.test import TestCase
from companysettings.models import InterviewStage
from ..factories._companysettings import InterviewStageFactory
from ..factories._companies import CompanyFactory


class InterviewStageModelTests(TestCase):

    def test_unicode(self):
        stage = InterviewStageFactory.build()
        self.assertEqual(unicode(stage), stage.name)

    def test_get_previous_stage_ok(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(company=company)
        stage2 = InterviewStageFactory(company=company)

        previous_stage = stage2.get_previous_stage()
        self.assertEqual(previous_stage, stage1)

    def test_get_previous_stage_none(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(company=company)

        previous_stage = stage1.get_previous_stage()
        self.assertIsNone(previous_stage)

    def test_get_next_stage_ok(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(company=company)
        stage2 = InterviewStageFactory(company=company)

        next_stage = stage1.get_next_stage()
        self.assertEqual(next_stage, stage2)

    def test_get_next_stage_none(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(company=company)

        next_stage = stage1.get_next_stage()
        self.assertIsNone(next_stage)

    def test_get_swap_position_ok(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(position=42, company=company)
        stage2 = InterviewStageFactory(position=7, company=company)

        old_stage1_position = stage1.position
        old_stage2_position = stage2.position

        result = stage1.swap_position(stage2)
        self.assertTrue(result)

        self.assertEqual(
            stage1.position,
            old_stage2_position
        )
        self.assertEqual(
            stage2.position,
            old_stage1_position
        )

    def test_get_swap_position_with_none(self):
        company = CompanyFactory()
        stage1 = InterviewStageFactory(company=company)

        old_stage1_position = stage1.position
        result = stage1.swap_position(None)

        self.assertFalse(result)
        self.assertEqual(
            stage1.position,
            old_stage1_position
        )