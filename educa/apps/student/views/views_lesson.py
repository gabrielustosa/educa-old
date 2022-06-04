import json

from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from educa.apps.content.models import Content
from educa.apps.course.models import CourseRelation
from educa.apps.lesson.models import Lesson
from educa.utils.mixin.course import CacheMixin


class SelectLessonView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/lesson/video.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_lesson'] = self.get_lesson()

        return context


class LessonNoteView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/modal_note.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item = Content.objects.get(id=self.kwargs.get('content_id')).item
        context['content'] = item.content

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


class CourseSearchView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/course/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_course()
        self.request.session[f'section-{course.id}'] = 'search'

        context['course'] = course

        return context


class CourseLessonSearchView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/course/search_content.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_course()

        search = request.POST.get('search')

        if search == "":
            return HttpResponse("<h5>Iniciar uma nova pesquisa</h5> <p>Para encontrar aulas deste curso.</p>")

        lessons = Lesson.objects.filter(course=course, title__icontains=search).all()

        if not lessons.exists():
            return HttpResponse("<h5>Não foi encontrado nenhum resultado para sua busca</h5>")

        context['lessons'] = lessons
        context['search'] = search

        return self.render_to_response(context)


class CourseUpdateCurrentLessonView(
    CsrfExemptMixin,
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        course = self.get_course()
        lesson_id = json.loads(request.body)['lesson_id']
        CourseRelation.objects.filter(course__id=course.id, user=request.user).update(current_lesson=lesson_id)
        return JsonResponse({'saved': 'ok'})