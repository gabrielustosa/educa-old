import pytest
from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.views import LoginView

from educa.apps.student.views import StudentRegisterView


@pytest.mark.fast
class StudentRegisterViewTest(TestCase):
    def test_student_register_view_is_correct(self):
        view = resolve(reverse('register'))
        self.assertEqual(view.func.view_class, StudentRegisterView)

    def test_student_register_view_returns_status_code_200(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_student_register_view_loads_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')


@pytest.mark.fast
class StudentLoginViewTest(TestCase):
    def test_student_loing_view_is_correct(self):
        view = resolve(reverse('login'))
        self.assertEqual(view.func.view_class, LoginView)

    def test_student_register_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_student_register_view_loads_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')
