import pytest

from educa.apps.module.views import ModuleCreateView, ModuleDeleteView, ModuleUpdateView
from tests.factories.course import CourseFactory
from tests.factories.module import ModuleFactory
from tests.base import TestCustomBase


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleCrudView(TestCustomBase):

    def test_module_create_view_is_correct(self):
        course = CourseFactory()

        self.login(is_superuser=True)

        view = self.get_view('module:create', kwargs={'course_id': course.id})
        self.assertIs(view.func.view_class, ModuleCreateView)

    def test_module_create_view_returns_status_code_200(self):
        course = CourseFactory()

        self.login(is_superuser=True)

        response = self.get_response('module:create', kwargs={'course_id': course.id})
        self.assertEqual(response.status_code, 200)

    def test_module_create_view_loads_correct_template(self):
        course = CourseFactory()

        self.login(is_superuser=True)

        response = self.get_response('module:create', kwargs={'course_id': course.id})
        self.assertTemplateUsed(response, 'module/create.html')

    def test_module_delete_view_is_correct(self):
        module = ModuleFactory()

        self.login(is_superuser=True)

        view = self.get_view('module:delete', kwargs={'module_id': module.id})
        self.assertIs(view.func.view_class, ModuleDeleteView)

    def test_module_delete_view_returns_status_code_200(self):
        module = ModuleFactory()

        self.login(is_superuser=True)

        response = self.get_response('module:delete', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 200)

    def test_create_delete_loads_correct_template(self):
        module = ModuleFactory()

        self.login(is_superuser=True)

        response = self.get_response('module:delete', kwargs={'module_id': module.id})
        self.assertTemplateUsed(response, 'module/delete.html')

    def test_module_update_view_is_correct(self):
        module = ModuleFactory()

        self.login(is_superuser=True)

        view = self.get_view('module:update', kwargs={'module_id': module.id})
        self.assertIs(view.func.view_class, ModuleUpdateView)

    def test_module_update_view_returns_status_code_200(self):
        module = ModuleFactory()

        self.login(is_superuser=True)

        response = self.get_response('module:update', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 200)

    def test_module_update_loads_correct_template(self):
        module = ModuleFactory()

        self.login(is_superuser=True)

        response = self.get_response('module:update', kwargs={'module_id': module.id})
        self.assertTemplateUsed(response, 'module/update.html')
