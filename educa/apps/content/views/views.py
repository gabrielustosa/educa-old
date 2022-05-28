from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.core.cache import cache

from educa.apps.lesson.models import Lesson
from educa.apps.mixin import CourseOwnerMixin
from educa.utils import content_is_instance


class LessonGetContentView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'hx/lesson/dynamic_content.html'

    def get_lesson(self):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = cache.get(f'lesson-{lesson_id}')
        if lesson:
            return lesson
        else:
            lesson = Lesson.objects.filter(id=lesson_id).first()
            cache.set(f'lesson-{lesson_id}', lesson)
            return lesson

    def get_course(self):
        return self.get_lesson().course

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        lesson = self.get_lesson()
        model_name = self.kwargs.get('model_name')
        contents = []

        for content in lesson.contents.all():
            if content_is_instance(content, model_name):
                contents.append(content)

        context['contents'] = contents
        context['lesson'] = lesson

        return context
