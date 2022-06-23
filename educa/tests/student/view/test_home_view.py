import pytest

from django.test import override_settings

from educa.apps.course.views.views import CourseListView
from educa.tests.base import TestCustomBase, TEST_CACHE_SETTING

from educa.tests.factories.course import CourseFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestHomeView(TestCustomBase):

    def test_home_view_is_correct(self):
        view = self.get_view('home')
        self.assertIs(view.func.view_class, CourseListView)

    def test_home_view_returns_status_code_200(self):
        response = self.response_get('home')
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_correct_template(self):
        response = self.response_get('home')
        self.assertTemplateUsed(response, 'course/list.html')

    @override_settings(CACHES=TEST_CACHE_SETTING)
    def test_home_template_loads_courses(self):
        course = CourseFactory()

        response = self.response_get('home')
        content = response.content.decode('utf-8')
        response_context_courses = response.context['courses']

        self.assertIn(course.title, content)
        self.assertEqual(len(response_context_courses), 1)

    def test_dont_show_my_courses_if_user_has_no_permission(self):
        response = self.response_get('home')
        content = response.content.decode('utf-8')

        self.assertNotIn(content, 'Meus cursos')
