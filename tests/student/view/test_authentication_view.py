import pytest

from django.contrib.auth.views import LoginView

from educa.apps.student.views import StudentRegisterView
from tests.base import TestCustomBase


@pytest.mark.fast
class StudentRegisterViewTest(TestCustomBase):
    def test_student_register_view_is_correct(self):
        view = self.get_view('register')
        self.assertEqual(view.func.view_class, StudentRegisterView)

    def test_student_register_view_returns_status_code_200(self):
        response = self.response_get('register')
        self.assertEqual(response.status_code, 200)

    def test_student_register_view_loads_correct_template(self):
        response = self.response_get('register')
        self.assertTemplateUsed(response, 'registration/register.html')


@pytest.mark.fast
class StudentLoginViewTest(TestCustomBase):
    def test_student_loing_view_is_correct(self):
        view = self.get_view('login')
        self.assertEqual(view.func.view_class, LoginView)

    def test_student_register_view_returns_status_code_200_OK(self):
        response = self.response_get('login')
        self.assertEqual(response.status_code, 200)

    def test_student_register_view_loads_correct_template(self):
        response = self.response_get('login')
        self.assertTemplateUsed(response, 'registration/login.html')
