import pytest
from parameterized import parameterized

from tests.base import TestCustomBase, ContentMixin
from tests.factories.lesson import LessonFactory
from tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestContentView(TestCustomBase, ContentMixin):

    @parameterized.expand(['text', 'file', 'image', 'link'])
    def test_anonymous_user_can_create_content(self, value):
        lesson = LessonFactory()

        response = self.response_get('content:create', kwargs={'lesson_id': lesson.id, 'model_name': value})
        self.assertEqual(response.status_code, 302)

    @parameterized.expand(['text', 'file', 'image', 'link'])
    def test_user_can_create_content_if_course_is_not_his_own(self, value):
        user = UserFactory(username='teste')
        lesson = LessonFactory(course__owner=user)

        self.login(is_superuser=True)

        response = self.response_get('content:create', kwargs={'lesson_id': lesson.id, 'model_name': value})
        self.assertEqual(response.status_code, 403)

    @parameterized.expand(['text', 'file', 'image', 'link'])
    def test_content_appear_only_for_course_owner(self, value):
        owner = UserFactory(username='teste')
        lesson = LessonFactory(module__course__owner=owner)
        self.create_content_in_batch(content_type=value, batch=4, lesson=lesson, owner=owner)

        self.login(is_superuser=True)

        response = self.response_get('content:get_content', kwargs={'lesson_id': lesson.id, 'model_name': value})

        response_context_contents = response.context['contents']

        self.assertEqual(len(response_context_contents), 4)

    @parameterized.expand(['text', 'file', 'image', 'link'])
    def test_user_can_delete_content_if_is_not_course_owner(self, value):
        owner = UserFactory(username='testes')
        lesson = LessonFactory(module__course__owner=owner, course__owner=owner)
        self.create_content(content_type=value, lesson=lesson, owner=owner)

        self.login(is_superuser=True)

        response = self.response_get('content:delete', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 403)

    @parameterized.expand(['text', 'file', 'image', 'link'])
    def test_user_can_update_content_if_is_not_course_owner(self, value):
        owner = UserFactory(username='teste')
        lesson = LessonFactory(module__course__owner=owner, course__owner=owner)
        obj = self.create_content(content_type=value, lesson=lesson, owner=owner)

        self.login(is_superuser=True)

        response = self.response_get('content:update',
                                     kwargs={'lesson_id': lesson.id, 'model_name': value, 'object_id': obj.id})
        self.assertEqual(response.status_code, 403)
