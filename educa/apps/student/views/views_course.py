from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from educa.apps.course.models import Course, CourseRelation
from educa.mixin import CacheMixin


class StudentCourseListView(TemplateView):
    template_name = 'student/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['courses'] = Course.objects.filter(students=self.request.user)

        return context


class StudentCourseView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'student/course_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        context['course'] = course
        context['modules'] = course.modules.all()
        context['current_lesson'] = self.get_lesson()

        match self.request.session.get(f'section-{course.id}'):
            case 'search':
                select = 'search'
            case 'overview':
                select = 'overview'
            case 'question':
                select = 'question'
            case 'notice':
                select = 'notice'
            case 'note':
                select = 'note'
            case 'rating':
                select = 'rating'
            case _:
                select = 'overview'

        context['select'] = select

        return context


class CourseEnrollView(
    CacheMixin,
    TemplateView,
):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        course = self.get_course()
        if request.user.is_anonymous:
            return redirect(reverse('login'))
        if CourseRelation.objects.filter(course=course, user=request.user).exists():
            messages.error(request, 'Você já está inscrito nesse curso.')
            return redirect(reverse('student:courses'))
        CourseRelation.objects.create(course=course, user=request.user, current_lesson=course.get_first_lesson().id)
        messages.success(request, f'Parabéns! Você agora você está inscrito no curso {course.title}!')
        return redirect(reverse('course:detail', kwargs={'course_id': course.id}))
