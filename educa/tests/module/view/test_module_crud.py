import pytest

from educa.tests.factories.course import CourseFactory
from educa.tests.factories.module import ModuleFactory
from educa.tests.factories.user import UserFactory
from educa.tests.base import TestCustomBase


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleCrud(TestCustomBase):
    def test_user_without_permission_can_view_create_module(self):
        course = CourseFactory()

        self.login()

        response = self.response_get('module:create', kwargs={'course_id': course.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_create_module_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        course = CourseFactory(owner=user)

        self.login()

        response = self.response_get('module:create', kwargs={'course_id': course.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_update_module(self):
        module = ModuleFactory()
        self.login()

        response = self.response_get('module:update', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_delete_module(self):
        module = ModuleFactory()
        self.login()

        response = self.response_get('module:delete', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_update_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        module = ModuleFactory(course__owner=user)

        self.login()

        response = self.response_get('module:update', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_delete_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        module = ModuleFactory(course__owner=user)

        self.login()

        response = self.response_get('module:delete', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)
