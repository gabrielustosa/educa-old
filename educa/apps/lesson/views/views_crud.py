from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.utils.mixin import CourseOwnerMixin
from educa.apps.module.models import Module
from educa.utils.utils import content_is_instance


class LessonCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    CreateView,
):
    template_name = 'lesson/create.html'
    model = Lesson
    fields = ['title', 'video']
    permission_required = 'lesson.add_lesson'

    @cached_property
    def get_module(self):
        module_id = self.kwargs.get('module_id')
        module = get_object_or_404(Module, id=module_id)
        return module

    def form_valid(self, form):
        module = self.get_module
        form.instance.module = module
        form.instance.course = module.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('module:detail', kwargs={'module_id': self.kwargs.get('module_id')})

    def get_course(self):
        return self.get_module.course


class LessonDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'lesson/detail.html'
    permission_required = 'lesson.view_lesson'

    @cached_property
    def get_lesson(self):
        lesson_id = get_object_or_404(Lesson, id=self.kwargs.get('lesson_id'))
        return lesson_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_lesson
        contents = Content.objects.filter(lesson=lesson).order_by('order')
        contents_list = []
        for content in contents:
            if content_is_instance(content, 'text'):
                contents_list.append(content)
        context['contents'] = contents_list
        context['lesson'] = lesson
        return context

    def get_course(self):
        return self.get_lesson.course


class LessonDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    DeleteView,
):
    template_name = 'lesson/delete.html'
    model = Lesson
    permission_required = 'lessons.delete_lesson'
    pk_url_kwarg = 'lesson_id'

    def get_success_url(self):
        module_id = self.get_object().module.id
        return reverse_lazy('module:detail', kwargs={'module_id': module_id})

    def get_course(self):
        return self.get_object().course


class LessonUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    UpdateView,
):
    template_name = 'lesson/create.html'
    model = Lesson
    fields = ['title', 'video']
    permission_required = 'lesson.change_lesson'
    pk_url_kwarg = 'lesson_id'

    def get_success_url(self):
        module_id = self.get_object().module.id
        return reverse_lazy('module:detail', kwargs={'module_id': module_id})

    def get_course(self):
        return self.get_object().course
