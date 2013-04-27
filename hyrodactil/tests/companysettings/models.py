from django.test import TestCase

from ..factories._companies import CompanyFactory
from ..factories._companysettings import InterviewStageFactory


class InterviewStageModelTests(TestCase):
    def setUp(self):
        company = CompanyFactory()
        # This will have position 1
        self.stage1 = InterviewStageFactory(company=company)
        # This will have position 2
        self.stage2 = InterviewStageFactory(name="Coding", company=company)

    def test_get_previous_stage_invalid(self):
        previous_stage = self.stage1.get_previous_stage()
        self.assertEqual(previous_stage, None)

    def test_get_previous_stage_valid(self):
        previous_stage = self.stage2.get_previous_stage()
        self.assertEqual(previous_stage, self.stage1)

    def test_get_next_stage_invalid(self):
        next_stage = self.stage2.get_next_stage()
        self.assertEqual(next_stage, None)

    def test_get_next_stage_valid(self):
        next_stage = self.stage1.get_next_stage()
        self.assertEqual(next_stage, self.stage2)

    def test_swap_stage_invalid(self):
        self.stage1.swap_position(None)
        self.assertEqual(self.stage1.position, 1)
        self.assertEqual(self.stage2.position, 2)

    def test_swap_stage_valid(self):
        self.stage1.swap_position(self.stage2)
        self.assertEqual(self.stage1.position, 2)
        self.assertEqual(self.stage2.position, 1)