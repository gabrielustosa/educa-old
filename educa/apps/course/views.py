from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from educa.apps.course.models import Course
from educa.apps.module.models import Module


class CourseListView(ListView):
    template_name = 'course/list.html'
    model = Course
    paginate_by = 6
    context_object_name = 'courses'


class CourseOwnerListView(
    LoginRequiredMixin,
    CourseListView,
):
    template_name = 'course/mine.html'

    def get_queryset(self):
        queryset = super(CourseOwnerListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class CourseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'course/create.html'
    model = Course
    fields = ['title', 'description', 'subject', 'image']
    success_url = reverse_lazy('course:mine')
    permission_required = 'courses.add_course'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    template_name = 'course/update.html'
    model = Course
    fields = ['title', 'description', 'subject', 'image']
    success_url = reverse_lazy('course:mine')
    permission_required = 'courses.change_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = Module.objects.filter(course=self.get_object())
        return context


class CourseDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    template_name = 'course/delete.html'
    model = Course
    success_url = reverse_lazy('course:mine')
    permission_required = 'courses.delete_course'
