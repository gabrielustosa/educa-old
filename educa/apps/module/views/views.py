from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.mixin import CourseOwnerMixin
from educa.apps.module.models import Module


class ModuleOrderView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    CsrfExemptMixin,
    TemplateView,
):
    template_name = 'hx/module/sortable.html'
    http_method_names = ['post']

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        modules_id = request.POST.getlist('module_id')
        for order, module_id in enumerate(modules_id, start=1):
            Module.objects.filter(id=module_id).update(order=order)

        context['modules'] = Module.objects.filter(course=self.get_course()).order_by('order').all()

        return self.render_to_response(context)
