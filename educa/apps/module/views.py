from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
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
        context['lessons'] = Lesson.objects.filter(module=module).order_by('order')
        context['module'] = module
        return context


@csrf_exempt
def module_order_view(request, course_id):
    course = Course.objects.get(id=course_id)
    if course.owner != request.user:
        raise PermissionDenied
    modules_id = request.POST.getlist('module_id')
    for order, module_id in enumerate(modules_id, start=1):
        Module.objects.filter(id=module_id).update(order=order)
    return render(request, 'hx/module_sortable.html',
                  context={
                      'modules': Module.objects.filter(course=course).order_by('order').all()
                  })
