from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from educa.utils.mixin.course import CourseOwnerMixin, CacheMixin
from educa.apps.module.models import Module


class ModuleOrderView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    CsrfExemptMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/module/sortable.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        modules_id = request.POST.getlist('module_id')
        for order, module_id in enumerate(modules_id, start=1):
            Module.objects.filter(id=module_id).update(order=order)

        context['modules'] = Module.objects.filter(course=self.get_course()).order_by('order').all()

        return self.render_to_response(context)
