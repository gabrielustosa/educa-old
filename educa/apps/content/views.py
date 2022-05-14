from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DeleteView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson


class ContentCreateUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    template_name = 'content/create.html'
    permission_required = 'content.add_content'
    lesson = None
    model = None
    object = None

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='content', model_name=model_name)
        return None

    def get_form(self, *args, **kwargs):
        form = modelform_factory(self.model, exclude=[
            'owner',
            'order',
            'created',
            'updated'
        ])
        return form(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, id=kwargs.get('lesson_id'))
        self.model = self.get_model(kwargs.get('model_name'))
        object_id = kwargs.get('object_id')
        if object_id:
            self.object = get_object_or_404(self.model, id=object_id)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()

        form = self.get_form(instance=self.object)

        context['form'] = form

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

        return render(request, self.template_name, context=context)


class ContentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    template_name = 'content/delete.html'
    model = Content
    permission_required = 'content.delete_content'

    def get_success_url(self):
        lesson_id = self.get_object().lesson.id
        return reverse_lazy('lesson:detail', kwargs={'lesson_id': lesson_id})
