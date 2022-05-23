import pytest
from django.urls import resolve, reverse

from educa.apps.module.views import ModuleDetailView

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

    def test_module_detail_view_is_correct(self):
        module = ModuleFactory()
        view = resolve(reverse('module:detail', kwargs={'module_id': module.id}))
        self.assertIs(view.func.view_class, ModuleDetailView)

    def test_module_datil_view_returns_status_code_200(self):
        module = ModuleFactory()
        self.login(is_superuser=True)
        response = self.client.get(reverse('module:detail', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 200)

    def test_my_course_view_loads_correct_template(self):
        module = ModuleFactory()
        self.login(is_superuser=True)
        response = self.client.get(reverse('module:detail', kwargs={'module_id': module.id}))
        self.assertTemplateUsed(response, 'module/detail.html')

    def test_module_detail_view_loads_only_lessons_own_module(self):
        module = ModuleFactory()
        LessonFactory(module=module)

        module_2 = ModuleFactory()

        self.login(is_superuser=True)

        response = self.client.get(reverse('module:detail', kwargs={'module_id': module_2.id}))
        response_context_lessons = response.context['lessons']

        self.assertEqual(len(response_context_lessons), 0)

    def test_user_without_permission_can_view_module_detail(self):
        module = ModuleFactory()
        self.login()

        response = self.client.get(reverse('module:detail', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_detail_if_is_not_his(self):
        user = UserFactory(username='teste')
        course = CourseFactory(owner=user)
        module = ModuleFactory(course=course)

        self.login(is_superuser=True)

        response = self.client.get(reverse('module:detail', kwargs={'module_id': module.id}))
        self.assertEqual(response.status_code, 403)
