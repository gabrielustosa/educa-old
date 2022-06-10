from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson
from educa.mixin import InstructorRequiredMixin, CacheMixin, HTMXRequireMixin


class LessonOrderView(
    HTMXRequireMixin,
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/lesson/sortable.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons_list = request.POST.getlist('lesson')

        order_list = [lesson.split('/')[1] for lesson in lessons_list]

        lesson_start = int(min(order_list))

        for order, lesson in enumerate(lessons_list, start=lesson_start):
            lesson_id = int(lesson.split('/')[0])
            Lesson.objects.filter(id=lesson_id).update(order=order)

        context['lessons'] = Lesson.objects.filter(module=self.get_module()).order_by('order').all()

        return self.render_to_response(context)

    def get_course(self):
        return self.get_module().course
