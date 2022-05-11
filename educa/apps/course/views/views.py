from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from educa.apps.course.models import Course


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


class CourseDetailView(TemplateView):
    template_name = 'course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])

        return context
