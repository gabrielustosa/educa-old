from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView

from educa.apps.course.models import Course, CourseRelation
from educa.apps.rating.models import Rating


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


@require_POST
def course_enrroll_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_anonymous:
        messages.error(request, 'Você precisa estar logado para se inscrever')
        return redirect(reverse('course:detail', kwargs={'course_id': course_id}))
    if CourseRelation.objects.filter(course=course, user=request.user).exists():
        messages.error(request, 'Você já está inscrito nesse curso.')
        return redirect(reverse('course:detail', kwargs={'course_id': course_id}))
    CourseRelation.objects.create(course=course, user=request.user, current_lesson=course.get_first_lesson_id())
    messages.success(request, f'Parabéns! Você agora você está inscrito no curso {course.title}!')
    return redirect(reverse('course:detail', kwargs={'course_id': course_id}))
