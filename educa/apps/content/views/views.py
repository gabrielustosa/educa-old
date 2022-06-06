from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from educa.mixin import CourseOwnerMixin, CacheMixin
from educa.utils.utils import content_is_instance


class LessonGetContentView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/lesson/dynamic_content.html'

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
