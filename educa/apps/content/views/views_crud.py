from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DeleteView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.mixin import CourseOwnerMixin
from educa.utils.utils import get_model


class ContentCreateUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'content/create.html'
    permission_required = 'content.add_content'
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

    def get_course(self):
        self.lesson = get_object_or_404(Lesson, id=self.kwargs.get('lesson_id'))
        return self.lesson.course


class ContentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    DeleteView,
):
    template_name = 'content/delete.html'
    model = Content
    permission_required = 'content.delete_content'
    pk_url_kwarg = 'lesson_id'

    def get_success_url(self):
        lesson_id = self.get_object().lesson.id
        return reverse_lazy('lesson:detail', kwargs={'lesson_id': lesson_id})

    def get_course(self):
        return self.get_object().lesson.course
