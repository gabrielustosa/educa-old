from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from educa.apps.lesson.models import Lesson
from educa.mixin import CourseOwnerMixin, CacheMixin
from educa.apps.module.models import Module


class ModuleCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    CacheMixin,
    CreateView,
):
    template_name = 'partials/crud/create_or_update.html'
    model = Module
    fields = ['title', 'description']
    success_url = reverse_lazy('course:mine')
    permission_required = 'module.add_module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Criando módulo'
        context['content_title'] = 'Criar módulo'
        context['button_label'] = 'Criar'

        return context

    def form_valid(self, form):
        form.instance.course = self.get_course()
        return super().form_valid(form)


class ModuleDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'module/detail.html'
    permission_required = 'module.view_module'

    def get_course(self):
        return self.get_module().course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_module()
        context['lessons'] = Lesson.objects.filter(module=module).order_by('order')
        context['module'] = module
        return context


class ModuleUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    UpdateView,
):
    template_name = 'partials/crud/create_or_update.html'
    model = Module
    fields = ['title', 'description']
    permission_required = 'module.change_course'
    pk_url_kwarg = 'module_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Editando módulo'
        context['content_title'] = 'Editar módulo'
        context['button_label'] = 'Salvar'

        return context

    def get_course(self):
        return self.get_object().course

    def get_success_url(self):
        return reverse_lazy('module:detail', kwargs={'module_id': self.kwargs.get('module_id')})


class ModuleDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    DeleteView,
):
    template_name = 'partials/crud/delete.html'
    model = Module
    permission_required = 'module.delete_course'
    pk_url_kwarg = 'module_id'
    success_url = reverse_lazy('course:mine')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.get_object()

        context['page_title'] = 'Detelando módulo'
        context['delete_message'] = f'Você tem certeza que deseja apagar o módulo "{obj.title}"?'
        context['cancel_url'] = reverse('module:detail', kwargs={'module_id': obj.id})

        return context

    def get_course(self):
        return self.get_object().course
