import pytest
from django.urls import reverse

from tests.factories.course import CourseFactory
from tests.factories.lesson import LessonFactory
from tests.factories.module import ModuleFactory
from tests.factories.user import UserFactory
from tests.base import TestAuthenticationBase


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleDdetailView(TestAuthenticationBase):
    @classmethod
    def setUpTestData(cls):
        cls.Module = ModuleFactory._meta.model
        cls.Lesson = LessonFactory._meta.model
        cls.Course = CourseFactory._meta.model
        cls.User = UserFactory._meta.model

    def test_user_without_permission_can_view_create_module(self):
        course = CourseFactory()
        self.login()

        response = self.client.get(reverse('module:create', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_update_module(self):
        module = ModuleFactory()
        self.login()

        response = self.client.get(reverse('module:update', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_delete_module(self):
        module = ModuleFactory()
        self.login()

        response = self.client.get(reverse('module:delete', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_update_if_is_not_his(self):
        user = UserFactory(username='teste')
        course = CourseFactory(owner=user)
        module = ModuleFactory(course=course)

        self.login(is_superuser=True)

        response = self.client.get(reverse('module:update', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_delete_if_is_not_his(self):
        user = UserFactory(username='teste')
        course = CourseFactory(owner=user)
        module = ModuleFactory(course=course)

        self.login(is_superuser=True)

        response = self.client.get(reverse('module:delete', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 403)
