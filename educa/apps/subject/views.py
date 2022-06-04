from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from educa.apps.course.models import Course
from educa.apps.course.views.views import CourseListView
from educa.apps.subject.models import Subject


class SubjectCourseView(CourseListView):

    @cached_property
    def get_subject(self):
        return get_object_or_404(Subject, id=self.kwargs.get('subject_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['subject'] = self.get_subject

        return context

    def get_queryset(self):
        subject = self.get_subject

        queryset = Course.objects.filter(subject=subject)

        return queryset
