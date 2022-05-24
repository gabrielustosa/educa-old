import pytest

from tests.base import TestCustomBase
from tests.factories.lesson import LessonFactory
from tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestLessonView(TestCustomBase):

    def test_user_without_permission_can_view_lesson_detail(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)
        self.login()

        response = self.get_response('lesson:detail', kwargs={'lesson_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_view_module_detail_if_course_is_not_his_own(self):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.get_response('lesson:detail', kwargs={'lesson_id': lesson.module.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cant_order_other_lessons(self):
        ...
