from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from educa.apps.course.models import Course
from educa.mixin import CourseOwnerMixin
from educa.apps.module.models import Module


class CourseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'course/create.html'
    model = Course
    fields = ['title', 'description', 'subject', 'image']
    success_url = reverse_lazy('course:mine')
    permission_required = 'course.add_course'

    def form_valid(self, form):
        course = self.get_object()
        course.instructors.add(self.request.user)
        user = self.request.user
        user.is_instructor = True
        user.save()
        return super().form_valid(form)


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
        return context

    def get_course(self):
        return self.get_object()


class CourseDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseOwnerMixin,
    DeleteView,
):
    template_name = 'course/delete.html'
    model = Course
    success_url = reverse_lazy('course:mine')
    permission_required = 'course.delete_course'
    pk_url_kwarg = 'course_id'

    def get_course(self):
        return self.get_object()
