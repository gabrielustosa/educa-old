import pytest

from educa.apps.lesson.views.views_manage import LessonCreateView, LessonDeleteView, LessonUpdateView
from tests.base import TestCustomBase
from tests.factories.lesson import LessonFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestLessonCrudView(TestCustomBase):
    def test_lesson_create_view_is_correct(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        view = self.get_view('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertIs(view.func.view_class, LessonCreateView)

    def test_lesson_create_view_returns_status_code_200(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        response = self.response_get('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 200)

    def test_lesson_create_view_loads_correct_template(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        response = self.response_get('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertTemplateUsed(response, 'lesson/create.html')

    def test_lesson_delete_view_is_correct(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        view = self.get_view('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertIs(view.func.view_class, LessonDeleteView)

    def test_lesson_delete_view_returns_status_code_200(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        response = self.response_get('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 200)

    def test_lesson_delete_loads_correct_template(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        response = self.response_get('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertTemplateUsed(response, 'lesson/delete.html')

    def test_lesson_update_view_is_correct(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        view = self.get_view('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertIs(view.func.view_class, LessonUpdateView)

    def test_lesson_update_view_returns_status_code_200(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        response = self.response_get('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 200)

    def test_lesson_update_loads_correct_template(self):
        lesson = LessonFactory()

        self.login(is_superuser=True)

        response = self.response_get('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertTemplateUsed(response, 'lesson/create.html')
