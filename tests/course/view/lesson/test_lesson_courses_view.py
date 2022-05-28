from educa.apps.course.models import CourseRelation
from educa.apps.lesson.models import Lesson
from educa.apps.student.views import StudentCourseView

from tests.base import TestCourseLessonMixin, TestCustomBase
from tests.factories.user import UserFactory


class TestCourseLessonView(TestCustomBase, TestCourseLessonMixin):

    def setUp(self):
        user = UserFactory(username='tester', password='tester')
        course = self.load_course()
        CourseRelation.objects.create(course=course, user=user, current_lesson=1)
        self.login(user)
        self.course = course
        self.response = self.response_get('student:view',
                                          kwargs={'course_id': self.course.id, 'lesson_id': 1})
        return super().setUp()

    def test_lesson_view_is_correct(self):
        view = self.get_view('student:view',
                             kwargs={'course_id': self.course.id, 'lesson_id': 1})
        self.assertIs(view.func.view_class, StudentCourseView)

    def test_lesson_view_returns_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_lesson_view_loads_correct_template(self):
        self.assertTemplateUsed(self.response, 'student/view.html')

    def test_if_course_modules_are_being_loaded_correctly(self):
        response_context_modules = self.response.context['modules']
        self.assertEqual(len(response_context_modules), 5)

    def test_if_course_lessons_are_being_loaded_correctly(self):
        response_context_modules = self.response.context['modules']
        self.assertEqual(len(response_context_modules.first().lessons.all()), 5)

    def test_if_course_contents_are_being_loaded_correctly(self):
        response_context_modules = self.response.context['modules']
        self.assertEqual(len(response_context_modules.first().lessons.first().contents.all()), 5)
