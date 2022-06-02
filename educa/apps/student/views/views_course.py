from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from educa.apps.course.models import Course, CourseRelation
from educa.apps.note.models import Note
from educa.apps.notice.models import Notice
from educa.apps.question.models import Question
from educa.apps.rating.models import Rating
from educa.settings import QUESTION_PAGINATE_BY
from educa.utils.mixin.course import CacheMixin


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

        context_object = None

        match self.request.session.get(f'section-{course.id}'):
            case 'search':
                template_section = 'hx/course/search.html'
            case 'overview':
                template_section = 'hx/course/overview.html'
            case 'question':
                template_section = 'hx/question/course/questions.html'
                objects = Question.objects.filter(lesson__course=course)
                paginator = Paginator(objects, QUESTION_PAGINATE_BY)
                context_object = paginator.page(1).object_list
                context['paginator'] = paginator
                context['page_obj'] = paginator.get_page(1)
                context['scroll_url'] = reverse('question_filter:all_questions', kwargs={'course_id': course.id})
            case 'notice':
                template_section = 'hx/notice/view.html'
                context_object = Notice.objects.filter(course=course)
            case 'note':
                template_section = 'hx/note/view.html'
                context_object = Note.objects.filter(user=self.request.user, lesson=self.get_lesson())
            case 'rating':
                template_section = 'hx/rating/rating.html'
                context_object = Rating.objects.filter(course=course)
            case _:
                template_section = 'hx/course/overview.html'

        context['template_section'] = template_section
        context['context_object'] = context_object

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
        CourseRelation.objects.create(course=course, user=request.user, current_lesson=course.get_first_lesson_id())
        messages.success(request, f'Parabéns! Você agora você está inscrito no curso {course.title}!')
        return redirect(reverse('course:detail', kwargs={'course_id': course.id}))
