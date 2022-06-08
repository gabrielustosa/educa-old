from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.mixin import InstructorRequiredMixin, CacheMixin
from educa.utils.utils import content_is_instance


class LessonCreateView(
    LoginRequiredMixin,
    CacheMixin,
    InstructorRequiredMixin,
    CreateView,
):
    template_name = 'partials/crud/create_or_update.html'
    model = Lesson
    fields = ['title', 'video']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Criando aula'
        context['content_title'] = 'Criar aula'
        context['button_label'] = 'Criar'

        return context

    def form_valid(self, form):
        module = self.get_module()
        form.instance.module = module
        form.instance.course = module.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('module:detail', kwargs={'module_id': self.kwargs.get('module_id')})

    def get_course(self):
        return self.get_module().course


class LessonDetailView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'lesson/detail.html'

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

    def get_course(self):
        return self.get_lesson().course


class LessonDeleteView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
    DeleteView,
):
    template_name = 'partials/crud/delete.html'
    model = Lesson
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Detelando aula'
        context['delete_message'] = f'Você tem certeza que deseja apagar a aula "{self.get_object().title}"?'
        context['cancel_url'] = self.get_success_url()

        return context

    def get_success_url(self):
        module_id = self.get_object().module.id
        return reverse_lazy('module:detail', kwargs={'module_id': module_id})

    def get_course(self):
        return self.get_object().course


class LessonUpdateView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
    UpdateView,
):
    template_name = 'partials/crud/create_or_update.html'
    model = Lesson
    fields = ['title', 'video']
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Editando aula'
        context['content_title'] = 'Editar aula'
        context['button_label'] = 'Salvar'

        return context

    def get_success_url(self):
        module_id = self.get_object().module.id
        return reverse_lazy('module:detail', kwargs={'module_id': module_id})

    def get_course(self):
        return self.get_object().course
