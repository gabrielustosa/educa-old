import pytest

from educa.tests.base import TestCustomBase
from educa.tests.factories.lesson import LessonFactory
from educa.tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestLessonView(TestCustomBase):

    def test_anonymouse_user_can_view_module_detail(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        response = self.response_get('lesson:detail', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 302)

    def test_user_without_permission_can_view_lesson_detail(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)
        self.login()

        response = self.response_get('lesson:detail', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_user_can_view_module_detail_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login()

        response = self.response_get('lesson:detail', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_can_order_other_lessons(self):
        lesson = LessonFactory()
        response = self.response_post('lesson:order', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_can_order_other_lessons_that_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(module__course__owner=user)

        self.login()

        response = self.response_post('lesson:order', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)
