import pytest

from educa.apps.module.views import ModuleDetailView

from tests.factories.course import CourseFactory
from tests.factories.lesson import LessonFactory
from tests.factories.module import ModuleFactory
from tests.factories.user import UserFactory
from tests.base import TestCustomBase


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleView(TestCustomBase):
    def setUp(self):
        self.module = ModuleFactory()
        return super().setUp()

    def test_module_detail_view_is_correct(self):
        view = self.get_view('module:detail', kwargs={'module_id': self.module.id})
        self.assertIs(view.func.view_class, ModuleDetailView)

    def test_module_detail_view_returns_status_code_200(self):
        self.login(is_superuser=True)
        response = self.response_get('module:detail', kwargs={'module_id': self.module.id})
        self.assertEqual(response.status_code, 200)

    def test_detail_view_loads_correct_template(self):
        self.login(is_superuser=True)
        response = self.response_get('module:detail', kwargs={'module_id': self.module.id})
        self.assertTemplateUsed(response, 'module/detail.html')

    def test_module_detail_view_loads_only_lessons_own_module(self):
        LessonFactory(module=self.module)

        module_2 = ModuleFactory()

        self.login(is_superuser=True)

        response = self.response_get('module:detail', kwargs={'module_id': module_2.id})
        response_context_lessons = response.context['lessons']

        self.assertEqual(len(response_context_lessons), 0)

    def test_anonymous_user_can_view_module_detail(self):
        response = self.response_get('module:detail', kwargs={'module_id': self.module.id})
        self.assertEqual(response.status_code, 302)

    def test_user_without_permission_can_view_module_detail(self):
        self.login()

        response = self.response_get('module:detail', kwargs={'module_id': self.module.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_module_detail_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        module = ModuleFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.response_get('module:detail', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 403)
