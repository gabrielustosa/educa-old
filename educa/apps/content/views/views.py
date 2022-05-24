from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson
from educa.apps.mixin import CourseOwnerMixin
from educa.utils import content_is_instance


class LessonGetContentView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'hx/lesson/dynamic_content.html'

    @cached_property
    def get_lesson(self):
        return get_object_or_404(Lesson, id=self.kwargs.get('lesson_id'))

    def get_course(self):
        return self.get_lesson.course

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        lesson = self.get_lesson
        model_name = self.kwargs.get('model_name')
        contents = []

        for content in lesson.contents.all():
            if content_is_instance(content, model_name):
                contents.append(content)

        context['contents'] = contents
        context['lesson'] = lesson

        return context
