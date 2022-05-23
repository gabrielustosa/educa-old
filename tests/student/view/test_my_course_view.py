import pytest
from django.urls import resolve, reverse

from educa.apps.course.views.views import CourseOwnerListView
from tests.base import TestAuthenticationBase
from tests.factories.course import CourseFactory
from tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestMyCourseView(TestAuthenticationBase):
    @classmethod
    def setUpTestData(cls):
        cls.Course = CourseFactory._meta.model
        cls.User = UserFactory._meta.model

    def test_my_course_view_is_correct(self):
        view = resolve(reverse('course:mine'))
        self.assertIs(view.func.view_class, CourseOwnerListView)

    def test_if_anonymous_user_cant_view_my_courses(self):
        response = self.client.get(reverse('course:mine'))
        self.assertEqual(response.status_code, 302)

    def test_my_course_view_loads_correct_template(self):
        self.login(is_superuser=True)
        response = self.client.get(reverse('course:mine'))
        self.assertTemplateUsed(response, 'course/mine.html')

    def test_my_course_view_loads_only_my_course_view(self):
        user = UserFactory(username='teste')

        CourseFactory(owner=user)

        self.login(is_superuser=True)
        response = self.client.get(reverse('course:mine'))
        response_context_courses = response.context['courses']

        self.assertEqual(len(response_context_courses), 0)

    def test_user_without_permission_can_create_course(self):
        self.login()
        response = self.client.get(reverse('course:create'))
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_update_course_if_is_not_his(self):
        user = UserFactory(username='teste')

        course = CourseFactory(owner=user)
        self.login(is_superuser=True)
        response = self.client.get(reverse('course:update', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_delete_course_if_is_not_his(self):
        user = UserFactory(username='teste')

        course = CourseFactory(owner=user)
        self.login(is_superuser=True)
        response = self.client.get(reverse('course:delete', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_update_course(self):
        user = UserFactory(username='teste')

        course = CourseFactory(owner=user)
        self.login()
        response = self.client.get(reverse('course:update', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_delete_course(self):
        user = UserFactory(username='teste')

        course = CourseFactory(owner=user)
        self.login()
        response = self.client.get(reverse('course:delete', kwargs={'course_id': course.id}))
        self.assertEqual(response.status_code, 403)
