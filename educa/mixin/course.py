from django.core.cache import cache
from django.core.exceptions import PermissionDenied

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.module.models import Module


class InstructorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        course = self.get_course()
        if request.user not in course.instructors.all():
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class HTMXRequireMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CacheMixin:
    def get_kwargs(self):
        return self.kwargs

    def get_lesson(self):
        lesson_id = self.get_kwargs().get('lesson_id')
        lesson = cache.get(f'lesson-{lesson_id}')
        if lesson:
            return lesson
        else:
            lesson = Lesson.objects.filter(id=lesson_id).first()
            cache.set(f'lesson-{lesson_id}', lesson)
            return lesson

    def get_module(self):
        module_id = self.get_kwargs().get('module_id')
        module = cache.get(f'module-{module_id}')
        if module:
            return module
        else:
            module = Module.objects.filter(id=module_id).first()
            cache.set(f'module-{module_id}', module)
            return module

    def get_course(self):
        course_id = self.get_kwargs().get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course



