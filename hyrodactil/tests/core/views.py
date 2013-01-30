from django.http import Http404
from django_webtest import WebTest

from companysettings.models import Department
from core.views import GetCompanyObjectsMixin
from ..factories._accounts import UserFactory
from ..factories._companysettings import DepartmentFactory


class CoreViewsTests(WebTest):
    class Request(object):
        """
        Class simulating a request object
        """
        def __init__(self, user):
            self.user = user

    def test_GetCompanyObjectsMixin_with_company(self):
        user = UserFactory()
        mixin = GetCompanyObjectsMixin()
        mixin.request = self.Request(user)
        mixin.model = Department
        department = DepartmentFactory(company=user.company)
        result = mixin.get_queryset()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], department)



    def test_GetCompanyObjectsMixin_without_company(self):
        user = UserFactory(company=None)
        mixin = GetCompanyObjectsMixin()
        mixin.request = self.Request(user)

        with self.assertRaises(Http404):
            mixin.get_queryset()
