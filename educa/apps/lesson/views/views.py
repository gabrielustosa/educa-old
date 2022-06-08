from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson
from educa.mixin import InstructorRequiredMixin, CacheMixin


class LessonOrderView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/lesson/sortable.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons = request.POST.getlist('lesson')
        for order, lesson_id in enumerate(lessons, start=1):
            Lesson.objects.filter(id=lesson_id).update(order=order)

        context['lessons'] = Lesson.objects.filter(module=self.get_module()).order_by('order').all()

        return self.render_to_response(context)

    def get_course(self):
        return self.get_module().course
