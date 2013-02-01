from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import Http404
from django_webtest import WebTest

from companysettings.models import Department
from core.views import MessageMixin, RestrictedListView
from ..factories._accounts import UserFactory
from ..factories._companysettings import DepartmentFactory


class CoreViewsTests(WebTest):
    class Request(object):
        """
        Class simulating a request object
        """
        def __init__(self, user=None):
            self.user = user

        def add_message_storage(self):
            self.session = {}
            self._message = FallbackStorage({'request': self})

    def test_ListCompanyObjectsMixin_with_company(self):
        user = UserFactory()
        mixin = RestrictedListView()
        mixin.request = self.Request(user)
        mixin.model = Department
        department = DepartmentFactory(company=user.company)
        result = mixin.get_queryset()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], department)

    def test_ListCompanyObjectsMixin_without_company(self):
        user = UserFactory(company=None)
        mixin = RestrictedListView()
        mixin.request = self.Request(user)

        with self.assertRaises(Http404):
            mixin.get_queryset()

    def test_UserAllowedActionMixin_with_company(self):
        user = UserFactory()
        mixin = RestrictedListView()
        mixin.request = self.Request(user)
        mixin.model = Department
        department = DepartmentFactory(company=user.company)
        result = mixin.get_queryset()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], department)

    def test_UserAllowedActionMixin_without_company(self):
        user = UserFactory(company=None)
        mixin = RestrictedListView()
        mixin.request = self.Request(user)

        with self.assertRaises(Http404):
            mixin.get_queryset()

    def _test_MessageMixin(self):
        mixin = MessageMixin()
        mixin.request = self.Request()
        mixin.request.add_message_storage()
        mixin.success_message = 'Test successful'
        mixin.form_valid(form=None)
        messages.get_messages(mixin.request)