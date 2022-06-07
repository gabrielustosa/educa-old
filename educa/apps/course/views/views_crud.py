from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from email_validator import validate_email, EmailSyntaxError

from educa.apps.course.models import Course
from educa.apps.student.models import User
from educa.mixin import CourseOwnerMixin
from educa.apps.module.models import Module


class CourseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'partials/crud/create_or_update.html'
    model = Course
    fields = ['title', 'description', 'subject', 'image', 'short_description', 'learn_description', 'requirements']
    success_url = reverse_lazy('course:mine')
    permission_required = 'course.add_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Criando curso'
        context['content_title'] = 'Criar curso'
        context['button_label'] = 'Criar'

        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user

        course = get_object_or_404(Course, id=form.instance.id)
        course.instructors.add(user)
        course.save()

        user.is_instructor = True
        user.save()
        return response


class CourseUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    UpdateView,
):
    template_name = 'course/update.html'
    model = Course
    fields = ['title', 'description', 'subject', 'image']
    success_url = reverse_lazy('course:mine')
    permission_required = 'course.change_course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['modules'] = Module.objects.filter(course=self.get_object())

        context['page_title'] = 'Editando curso'
        context['content_title'] = 'Editar curso'
        context['button_label'] = 'Salvar'

        return context

    def form_valid(self, form):
        instructor = self.request.POST.get('instructor')

        if instructor == '':
            return super().form_valid(form)

        try:
            validate_email(instructor)
            try:
                user = User.objects.get(email=instructor)

                course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
                if course.instructors.filter(id=user.id).exists():
                    return super().form_invalid(form)

                course.instructors.add(user)

                user.is_instructor = True
                user.save()
            except ObjectDoesNotExist:
                return super().form_invalid(form)
            return super().form_valid(form)
        except EmailSyntaxError:
            return super().form_invalid(form)

    def get_course(self):
        return self.get_object()


class CourseDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    DeleteView,
):
    template_name = 'partials/crud/delete.html'
    model = Course
    success_url = reverse_lazy('course:mine')
    permission_required = 'course.delete_course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.get_object()

        context['page_title'] = 'Detelando curso'
        context['delete_message'] = f'Você tem certeza que deseja apagar o curso "{obj.title}"?'
        context['cancel_url'] = self.get_success_url()

        return context

    def get_course(self):
        return self.get_object()
