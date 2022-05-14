from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
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


@require_POST
def course_enrroll_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_anonymous:
        messages.error(request, 'Você precisa estar logado para se inscrever')
        return redirect(reverse('course:detail', kwargs={'course_id': course_id}))
    if Course.objects.filter(id=course_id).filter(students=request.user).exists():
        messages.error(request, 'Você já está inscrito nesse curso.')
        return redirect(reverse('course:detail', kwargs={'course_id': course_id}))
    course.students.add(request.user)
    messages.success(request, f'Parabéns! Você agora você está inscrito no curso {course.title}!')
    return redirect(reverse('course:detail', kwargs={'course_id': course_id}))
