import pytest

from educa.tests.base import TestCustomBase
from educa.tests.factories.lesson import LessonFactory
from educa.tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestLessonCrudView(TestCustomBase):
    def test_user_without_permission_can_view_create_lesson(self):
        lesson = LessonFactory()
        self.login()

        response = self.response_get('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_create_lesson_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(module__course__owner=user)

        self.login()

        response = self.response_get('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_update_lesson(self):
        lesson = LessonFactory()
        self.login()

        response = self.response_get('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_can_view_delete_lesson(self):
        lesson = LessonFactory()
        self.login()

        response = self.response_get('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_lesson_update_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login()

        response = self.response_get('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_owner_cant_view_lesson_delete_if_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login()

        response = self.response_get('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)
