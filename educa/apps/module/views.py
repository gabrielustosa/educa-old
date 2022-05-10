from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import CreateView, TemplateView

from educa.apps.content.models import Content
from educa.apps.course.models import Course
from educa.apps.module.models import Module


class ModuleCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'module/create.html'
    model = Module
    fields = ['title', 'description']
    success_url = reverse_lazy('course:mine')
    permission_required = 'module.add_module'

    def get_course(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course

    def form_valid(self, form):
        form.instance.course = self.get_course()
        return super().form_valid(form)


class ModuleDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    template_name = 'module/detail.html'
    permission_required = 'module.view_module'

    def get_module(self):
        module_id = get_object_or_404(Module, id=self.kwargs.get('module_id'))
        return module_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_module()
        context['contents'] = Content.objects.filter(module=module).order_by('order')
        context['module'] = module
        return context


class ModuleOrderView(
    CsrfExemptMixin,
    JsonRequestResponseMixin,
    TemplateView
):
    def post(self, request):
        for module_id, order in self.request_json.items():
            Module.objects.filter(id=module_id).update(order=order)
        return self.render_json_response({'saved': 'OK'})
