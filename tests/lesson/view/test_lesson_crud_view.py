import pytest

from tests.base import TestCustomBase
from tests.factories.course import CourseFactory
from tests.factories.lesson import LessonFactory
from tests.factories.module import ModuleFactory
from tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestLessonCrud(TestCustomBase):
    def test_user_without_permission_can_view_create_module(self):
        lesson = LessonFactory()
        self.login()

        response = self.get_response('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_create_lesson_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(module__course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_update_lesson(self):
        lesson = LessonFactory()
        self.login()

        response = self.get_response('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_delete_lesson(self):
        module = LessonFactory()
        self.login()

        response = self.get_response('lesson:delete', kwargs={'lesson_id': module.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_lesson_update_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_lesson_delete_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_view_module_detail_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('lesson:detail', kwargs={'lesson_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)
