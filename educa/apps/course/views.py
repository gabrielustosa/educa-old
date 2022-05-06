from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, TemplateView

from educa.apps.course.models import Course


class CourseListView(ListView):
    template_name = 'course/list.html'
    model = Course
    paginate_by = 6
    context_object_name = 'courses'


class CourseOwnerList(
    CourseListView,
    LoginRequiredMixin,
    PermissionRequiredMixin,
):
    template_name = 'course/mine.html'

    def get_queryset(self):
        queryset = super(CourseOwnerList, self).get_queryset()
        return queryset.filter(owner=self.request.user)


