from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.apps.module.models import Module
from educa.utils import content_is_instance


class LessonCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'lesson/create.html'
    model = Lesson
    fields = ['title', 'video']
    permission_required = 'lesson.add_lesson'

    def get_module(self):
        module_id = self.kwargs.get('module_id')
        module = get_object_or_404(Module, id=module_id)
        return module

    def form_valid(self, form):
        form.instance.module = self.get_module()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('module:detail', kwargs={'module_id': self.kwargs.get('module_id')})


class LessonDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    template_name = 'lesson/delete.html'
    model = Lesson
    permission_required = 'lessons.delete_lesson'

    def get_success_url(self):
        module_id = self.get_object().module.id
        return reverse_lazy('module:detail', kwargs={'module_id': module_id})


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
        contents = Content.objects.filter(lesson=lesson).order_by('order')
        contents_list = []
        for content in contents:
            if content_is_instance(content, 'text'):
                contents_list.append(content)
        context['contents'] = contents_list
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
    permission_required = 'lesson.change_lesson'

    def get_success_url(self):
        module_id = self.get_object().module.id
        return reverse_lazy('module:detail', kwargs={'module_id': module_id})


@csrf_exempt
def lesson_order_view(request, module_id):
    module = Module.objects.get(id=module_id)
    if module.course.owner != request.user:
        raise PermissionDenied
    lessons_id = request.POST.getlist('lesson_id')
    for order, lesson_id in enumerate(lessons_id, start=1):
        Lesson.objects.filter(id=lesson_id).update(order=order)
    return render(request, 'hx/lesson/lesson_sortable.html',
                  context={
                      'lessons': Lesson.objects.filter(module=module).order_by('order').all()
                  })


def lesson_content_view(request, lesson_id, class_name):
    lesson = Lesson.objects.get(id=lesson_id)
    contents = []
    for content in lesson.contents.all():
        if content_is_instance(content, class_name):
            contents.append(content)
    return render(request, 'hx/lesson/lesson_dynamic_content.html', context={'contents': contents, 'lesson': lesson})
