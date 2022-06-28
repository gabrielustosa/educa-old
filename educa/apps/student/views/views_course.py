from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from educa.apps.course.models import Course, CourseRelation
from educa.apps.lesson.models import LessonRelation, Lesson
from educa.mixin import CacheMixin


class StudentCourseListView(LoginRequiredMixin, TemplateView):
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
        course = Course.objects.filter(id=self.kwargs.get('course_id')).annotate(total_lessons=Count('lesson')).first()
        current_lesson = self.get_lesson()

        if not course or not current_lesson:
            raise Http404()

        context['course'] = course

        context['relations'] = LessonRelation.objects \
            .filter(user=self.request.user,
                    lesson__course=course).prefetch_related('lesson__module').all()

        context['modules'] = course.modules.annotate(
            total_lessons=Count('lessons'),
            total_video_duration=Sum('lessons__video_duration')).prefetch_related('lessons').order_by('order').all()

        context['lessons'] = Lesson.objects.filter(course=course).order_by('order').select_related(
            'module').prefetch_related('contents').all()

        context['current_lesson'] = current_lesson

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
