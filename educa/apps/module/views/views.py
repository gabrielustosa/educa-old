from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from educa.mixin import InstructorRequiredMixin, CacheMixin, HTMXRequireMixin
from educa.apps.module.models import Module


class ModuleOrderView(
    HTMXRequireMixin,
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/module/sortable.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        modules_id = request.POST.getlist('module_id')

        lesson_last = 1
        for order, module_id in enumerate(modules_id, start=1):
            Module.objects.filter(id=module_id).update(order=order)

            module = Module.objects.get(id=module_id)

            for lesson_order, lesson in enumerate(module.lessons.order_by('order').all(), start=lesson_last):
                lesson.order = lesson_order
                lesson.save()

            lesson_order_list = [lesson.order for lesson in module.lessons.all()]
            lesson_max = int(max(lesson_order_list))

            lesson_last = lesson_max + 1

        context['modules'] = Module.objects.filter(course=self.get_course()).order_by('order').all()

        return self.render_to_response(context)
