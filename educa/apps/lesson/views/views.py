from braces.views import CsrfExemptMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson
from educa.apps.mixin import CourseOwnerMixin
from educa.apps.module.models import Module
from educa.utils import content_is_instance


class LessonOrderView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    CsrfExemptMixin,
    TemplateView,
):
    template_name = 'hx/lesson/sortable.html'

    @cached_property
    def get_module(self):
        return get_object_or_404(Module, id=self.kwargs.get('module_id'))

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons = request.POST.getlist('lesson')
        for order, lesson_id in enumerate(lessons, start=1):
            Lesson.objects.filter(id=lesson_id).update(order=order)

        context['lessons'] = Lesson.objects.filter(module=self.get_module).order_by('order').all()

        return self.render_to_response(context)

    def get_course(self):
        return self.get_module.course
