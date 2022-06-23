import pytest

from educa.apps.lesson.views.views_crud import LessonCreateView, LessonDeleteView, LessonUpdateView
from educa.tests.base import TestCustomBase
from educa.tests.factories.lesson import LessonFactory
from educa.tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestLessonCrudView(TestCustomBase):
    def test_lesson_create_view_is_correct(self):
        lesson = LessonFactory()

        self.login()

        view = self.get_view('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertIs(view.func.view_class, LessonCreateView)

    def test_lesson_create_view_returns_status_code_200(self):
        tester = UserFactory()
        lesson = LessonFactory(module__course__owner=tester)
        self.login(email=tester.email)

        response = self.response_get('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertEqual(response.status_code, 200)

    def test_lesson_create_view_loads_correct_template(self):
        tester = UserFactory()
        lesson = LessonFactory(module__course__owner=tester)
        self.login(email=tester.email)

        response = self.response_get('lesson:create', kwargs={'module_id': lesson.module.id})
        self.assertTemplateUsed(response, 'partials/crud/create_or_update.html')

    def test_lesson_delete_view_is_correct(self):
        lesson = LessonFactory()

        self.login()

        view = self.get_view('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertIs(view.func.view_class, LessonDeleteView)

    def test_lesson_delete_view_returns_status_code_200(self):
        tester = UserFactory()
        lesson = LessonFactory(course__owner=tester)
        self.login(email=tester.email)

        response = self.response_get('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 200)

    def test_lesson_delete_loads_correct_template(self):
        tester = UserFactory()
        lesson = LessonFactory(course__owner=tester)
        self.login(email=tester.email)

        response = self.response_get('lesson:delete', kwargs={'lesson_id': lesson.id})
        self.assertTemplateUsed(response, 'partials/crud/delete.html')

    def test_lesson_update_view_is_correct(self):
        lesson = LessonFactory()

        self.login()

        view = self.get_view('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertIs(view.func.view_class, LessonUpdateView)

    def test_lesson_update_view_returns_status_code_200(self):
        tester = UserFactory()
        lesson = LessonFactory(course__owner=tester)
        self.login(email=tester.email)

        response = self.response_get('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertEqual(response.status_code, 200)

    def test_lesson_update_loads_correct_template(self):
        tester = UserFactory()
        lesson = LessonFactory(course__owner=tester)
        self.login(email=tester.email)

        response = self.response_get('lesson:update', kwargs={'lesson_id': lesson.id})
        self.assertTemplateUsed(response, 'partials/crud/create_or_update.html')
