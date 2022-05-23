import pytest
from django.test import TestCase
from django.urls import resolve, reverse

from educa.apps.course.views.views import CourseListView

from tests.factories.course import CourseFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Course = CourseFactory._meta.model

    def test_home_view_is_correct(self):
        view = resolve(reverse('home'))
        self.assertIs(view.func.view_class, CourseListView)

    def test_home_view_returns_status_code_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'course/list.html')

    def test_home_template_shows_no_courses_found_if_no_courses(self):
        response = self.client.get(reverse('home'))
        self.assertIn(
            'Nenhum curso foi encontrado :(',
            response.content.decode('utf-8')
        )

    def test_home_template_loads_courses(self):
        course = CourseFactory()

        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        response_context_courses = response.context['courses']

        self.assertIn(course.title, content)
        self.assertEqual(len(response_context_courses), 1)

    def test_dont_show_my_courses_if_user_has_no_permission(self):
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')

        self.assertNotIn(content, 'Meus cursos')
