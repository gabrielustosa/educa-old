import json

from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from educa.apps.content.models import Content
from educa.apps.course.models import CourseRelation, Course
from educa.apps.lesson.models import Lesson
from educa.apps.module.models import Module
from educa.apps.module.module import ModuleObject, LessonObject
from educa.mixin import CacheMixin


class SelectLessonView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/lesson/video.html'

    def get_kwargs(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_lesson'] = self.get_lesson()

        return context


class LessonNoteView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/modal/note_body.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item = Content.objects.get(id=self.kwargs.get('content_id')).item
        context['content'] = item.content

        return context


class CourseOverView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = 'hx/course/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = Course.objects.filter(id=self.kwargs.get('course_id')) \
            .annotate(total_video_duration=Sum('lesson__video_duration')) \
            .annotate(total_students=Count('students')).prefetch_related('modules').first()

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
            return HttpResponse(
                '<h5 class="text-center text-3xl font-bold">Iniciar uma nova pesquisa</h5> <p class="text-center text-lg">Para encontrar aulas ou módulos</p>')

        lessons_query = Lesson.objects.filter(course=course, title__icontains=search).select_related('module').all()

        modules_query = Module.objects.filter(title__icontains=search).all()

        if not lessons_query.exists() and not modules_query.exists():
            return HttpResponse(
                f'<h5 class="text-center text-2xl font-bold">Nenhum resultado encontrado para "{search}"</h5> <p class="text-center text-lg">Sua pesquisa não correspondeu com nenhuma aula</p> ')

        modules = []

        for module in modules_query:
            module_object = ModuleObject(
                id_=module.id,
                title=module.title,
                order=module.order
            )
            modules.append(module_object)

        for lesson in lessons_query:
            lesson_module = lesson.module
            lesson_object = LessonObject(
                id_=lesson.id,
                title=lesson.title,
                order=lesson.order,
                video_duration=lesson.video_duration
            )
            by_id = list(filter(lambda m: m.id == lesson_module.id, modules))
            if by_id:
                module = by_id[0]
                module.video_duration += lesson.video_duration
                module.add_lesson(lesson_object)
            else:
                module_object = ModuleObject(
                    id_=lesson_module.id,
                    title=lesson_module.title,
                    order=lesson_module.order,
                    video_duration=lesson.video_duration
                )
                module_object.add_lesson(lesson_object)
                modules.append(module_object)

        context['modules'] = modules
        context['total_lessons'] = lessons_query.count()
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
