import pytest

from educa.apps.module.views.views_crud import ModuleCreateView, ModuleDeleteView, ModuleUpdateView
from educa.tests.factories.course import CourseFactory
from educa.tests.factories.module import ModuleFactory
from educa.tests.base import TestCustomBase
from educa.tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleCrudView(TestCustomBase):

    def test_module_create_view_is_correct(self):
        tester = UserFactory()
        course = CourseFactory(owner=tester)

        self.login(email=tester.email)

        view = self.get_view('module:create', kwargs={'course_id': course.id})
        self.assertIs(view.func.view_class, ModuleCreateView)

    def test_module_create_view_returns_status_code_200(self):
        tester = UserFactory()
        course = CourseFactory(owner=tester)

        self.login(email=tester.email)

        response = self.response_get('module:create', kwargs={'course_id': course.id})
        self.assertEqual(response.status_code, 200)

    def test_module_create_view_loads_correct_template(self):
        tester = UserFactory()
        course = CourseFactory(owner=tester)

        self.login(email=tester.email)

        response = self.response_get('module:create', kwargs={'course_id': course.id})
        self.assertTemplateUsed(response, 'partials/crud/create_or_update.html')

    def test_module_delete_view_is_correct(self):
        module = ModuleFactory()

        self.login()

        view = self.get_view('module:delete', kwargs={'module_id': module.id})
        self.assertIs(view.func.view_class, ModuleDeleteView)

    def test_module_delete_view_returns_status_code_200(self):
        tester = UserFactory()
        module = ModuleFactory(course__owner=tester)

        self.login(email=tester.email)

        response = self.response_get('module:delete', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 200)

    def test_module_delete_loads_correct_template(self):
        tester = UserFactory()
        module = ModuleFactory(course__owner=tester)

        self.login(email=tester.email)

        response = self.response_get('module:delete', kwargs={'module_id': module.id})
        self.assertTemplateUsed(response, 'partials/crud/delete.html')

    def test_module_update_view_is_correct(self):
        tester = UserFactory()
        module = ModuleFactory(course__owner=tester)

        self.login(email=tester.email)

        view = self.get_view('module:update', kwargs={'module_id': module.id})
        self.assertIs(view.func.view_class, ModuleUpdateView)

    def test_module_update_view_returns_status_code_200(self):
        tester = UserFactory()
        module = ModuleFactory(course__owner=tester)

        self.login(email=tester.email)

        response = self.response_get('module:update', kwargs={'module_id': module.id})
        self.assertEqual(response.status_code, 200)

    def test_module_update_loads_correct_template(self):
        tester = UserFactory()
        module = ModuleFactory(course__owner=tester)

        self.login(email=tester.email)

        response = self.response_get('module:update', kwargs={'module_id': module.id})
        self.assertTemplateUsed(response, 'partials/crud/create_or_update.html')
