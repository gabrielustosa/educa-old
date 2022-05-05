from django.test import TestCase
from django.urls import resolve, reverse

from educa.apps.student.views import StudentRegisterView


class StudentRegisterViewTest(TestCase):
    def test_student_register_view_is_correct(self):
        view = resolve(reverse('register'))
        self.assertEqual(view.func.view_class, StudentRegisterView)

    def test_student_register_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_student_register_view_loads_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')
