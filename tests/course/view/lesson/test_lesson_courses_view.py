from educa.apps.student.views import StudentCourseView
from tests.base import CourseLessonMixin, TestCustomBase


class TestCourseLessonView(CourseLessonMixin, TestCustomBase):

    def test_home_view_is_correct(self):
        view = self.get_view('student:view',
                             kwargs={'course_slug': self.course.slug, 'lesson_id': self.get_lesson_by_id(1).id})
        self.assertIs(view.func.view, StudentCourseView)

    def test_home_view_returns_status_code_200(self):
        response = self.response_get('student:view',
                                     kwargs={'course_slug': self.course.slug, 'lesson_id': self.get_lesson_by_id(1).id})
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_correct_template(self):
        response = self.response_get('student:view',
                                     kwargs={'course_slug': self.course.slug, 'lesson_id': self.get_lesson_by_id(1).id})
        self.assertTemplateUsed(response, 'student/view.html')

    def test_if_course_modules_are_being_loaded_correctly(self):
        response = self.response_get('student:view',
                                     kwargs={'course_slug': self.course.slug, 'lesson_id': self.get_lesson_by_id(1).id})
        response_context_modules = response.context['modules']
        self.assertEqual(len(response_context_modules), 5)

    def test_if_course_lessons_are_being_loaded_correctly(self):
        response = self.response_get('student:view',
                                     kwargs={'course_slug': self.course.slug, 'lesson_id': self.get_lesson_by_id(1).id})
        response_context_modules = response.context['modules']
        self.assertEqual(len(response_context_modules.first().lessons.all()), 5)

    def test_if_course_contents_are_being_loaded_correctly(self):
        response = self.response_get('student:view',
                                     kwargs={'course_slug': self.course.slug, 'lesson_id': self.get_lesson_by_id(1).id})
        response_context_modules = response.context['modules']
        self.assertEqual(len(response_context_modules.first().lessons.first().contents.all()), 5)
