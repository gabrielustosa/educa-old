from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.apps.module.models import Module


class LessonCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'lesson/create.html'
    model = Lesson
    fields = ['title', 'video']
    success_url = reverse_lazy('course:mine')
    permission_required = 'lesson.add_lesson'

    def get_module(self):
        module_id = self.kwargs.get('module_id')
        module = get_object_or_404(Module, id=module_id)
        return module

    def form_valid(self, form):
        form.instance.module = self.get_module()
        return super().form_valid(form)


class LessonDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    template_name = 'lesson/delete.html'
    model = Lesson
    success_url = reverse_lazy('course:mine')
    permission_required = 'lessons.delete_lesson'


class LessonDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    template_name = 'lesson/detail.html'
    permission_required = 'lesson.view_lesson'

    def get_lesson(self):
        lesson_id = get_object_or_404(Lesson, id=self.kwargs.get('lesson_id'))
        return lesson_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_lesson()
        context['contents'] = Content.objects.filter(lesson=lesson).order_by('order')
        context['lesson'] = lesson
        return context


class LessonUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    template_name = 'lesson/create.html'
    model = Lesson
    fields = ['title', 'video']
    success_url = reverse_lazy('course:mine')
    permission_required = 'lesson.change_lesson'


@csrf_exempt
def lesson_order_view(request):
    lessons_id = request.POST.getlist('lesson_id')
    for order, lesson_id in enumerate(lessons_id, start=1):
        Lesson.objects.filter(id=lesson_id).update(order=order)
    return render(request, 'hx/lesson_sortable.html',
                  context={
                      'lessons': Lesson.objects.filter(module__course__owner=request.user).order_by('order').all()
                  })
