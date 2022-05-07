from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from educa.apps.course.models import Course


class CourseListView(ListView):
    template_name = 'course/list.html'
    model = Course
    paginate_by = 6
    context_object_name = 'courses'


class CourseOwnerList(
    LoginRequiredMixin,
    CourseListView,
):
    template_name = 'course/mine.html'

    def get_queryset(self):
        queryset = super(CourseOwnerList, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class CourseOwnerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    template_name = 'course/create.html'
    model = Course
    fields = ['subject', 'title', 'description', 'image']
    success_url = reverse_lazy('course:mine')
    permission_required = 'courses.add_course'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
