from braces.views import CsrfExemptMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson
from educa.apps.mixin import CourseOwnerMixin
from educa.apps.module.models import Module


class LessonOrderView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    CsrfExemptMixin,
    TemplateView,
):
    template_name = 'hx/lesson/sortable.html'
    http_method_names = ['post']

    def get_module(self):
        module_id = self.kwargs.get('module_id')
        module = cache.get(f'module-{module_id}')
        if module:
            return module
        else:
            module = Module.objects.filter(id=module_id).first()
            cache.set(f'module-{module_id}', module)
            return module

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons = request.POST.getlist('lesson')
        for order, lesson_id in enumerate(lessons, start=1):
            Lesson.objects.filter(id=lesson_id).update(order=order)

        context['lessons'] = Lesson.objects.filter(module=self.get_module()).order_by('order').all()

        return self.render_to_response(context)

    def get_course(self):
        return self.get_module().course
