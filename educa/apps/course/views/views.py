from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from educa.apps.course.models import Course
from educa.apps.rating.models import Rating
from educa.utils.mixin.course import CacheMixin


class CourseListView(ListView):
    template_name = 'course/list.html'
    model = Course
    paginate_by = 6
    context_object_name = 'courses'


class CourseOwnerListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CourseListView,
):
    template_name = 'course/mine.html'
    permission_required = 'course.add_course'

    def get_queryset(self):
        queryset = super(CourseOwnerListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class CourseDetailView(TemplateView):
    template_name = 'course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        context['course'] = course
        context['ratings'] = Rating.objects.filter(course=course)

        return context


class CourseOverView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/course/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_course()
        context['course'] = course
        self.request.session[f'section-{course.id}'] = 'overview'

        return context
