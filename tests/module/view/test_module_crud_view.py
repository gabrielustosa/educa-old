import pytest

from tests.factories.course import CourseFactory
from tests.factories.module import ModuleFactory
from tests.factories.user import UserFactory
from tests.base import TestCustomBase


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleCrudView(TestCustomBase):
    def test_user_without_permission_can_view_create_module(self):
        course = CourseFactory()

        self.login()

        response = self.get_response('module:create', kwargs={'course_id': course.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_create_module_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        course = CourseFactory(owner=user)

        self.login(is_superuser=True)

        response = self.get_response('module:create', kwargs={'course_id': course.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_update_module(self):
        module = ModuleFactory()
        self.login()

        response = self.get_response('module:update', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_delete_module(self):
        module = ModuleFactory()
        self.login()

        response = self.get_response('module:delete', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_update_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        module = ModuleFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('module:update', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_delete_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        module = ModuleFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('module:delete', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)
