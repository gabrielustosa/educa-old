from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DeleteView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.mixin import InstructorRequiredMixin
from educa.utils.utils import get_model


class ContentCreateUpdateView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
    TemplateView,
):
    template_name = 'partials/crud/create_or_update.html'
    lesson = None
    model = None
    object = None

    def get_form(self, *args, **kwargs):
        form = modelform_factory(self.model, exclude=[
            'owner',
            'order',
            'created',
            'updated'
        ])
        return form(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.model = get_model(kwargs.get('model_name'))
        object_id = kwargs.get('object_id')
        if object_id:
            self.object = get_object_or_404(self.model, id=object_id)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()

        form = self.get_form(instance=self.object)

        context['form'] = form

        if self.kwargs.get('object_id'):
            context['page_title'] = 'Editando conteúdo'
            context['content_title'] = 'Editar conteúdo'
            context['button_label'] = 'Salvar'
        else:
            context['page_title'] = 'Criando conteúdo'
            context['content_title'] = 'Criar conteúdo'
            context['button_label'] = 'Criar'

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(
            instance=self.object,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not self.kwargs.get('object_id'):
                Content.objects.create(
                    lesson=self.lesson,
                    item=obj
                )
            return redirect(reverse('lesson:detail', kwargs={'lesson_id': self.lesson.id}))

        context = super().get_context_data()
        context['form'] = form
        context['object'] = self.object
        context['button_label'] = 'Salvar'

        return render(request, self.template_name, context=context)

    def get_course(self):
        self.lesson = get_object_or_404(Lesson, id=self.kwargs.get('lesson_id'))
        return self.lesson.course


class ContentDeleteView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
    DeleteView,
):
    template_name = 'partials/crud/delete.html'
    model = Content
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Detelando contéudo'
        context['delete_message'] = f'Você tem certeza que deseja apagar o conteúdo "{self.get_object().item.title}"?'
        context['cancel_url'] = self.get_success_url()

        return context

    def get_success_url(self):
        lesson_id = self.get_object().lesson.id
        return reverse_lazy('lesson:detail', kwargs={'lesson_id': lesson_id})

    def get_course(self):
        return self.get_object().lesson.course
