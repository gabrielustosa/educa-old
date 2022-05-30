import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from educa.apps.content.models import Content
from educa.apps.course.models import Course, CourseRelation
from educa.apps.lesson.models import Lesson
from educa.apps.student.forms import UserCreateForm


class StudentRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(request=self.request, user=user)
        return result


class StudentCourseListView(TemplateView):
    template_name = 'student/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['courses'] = Course.objects.filter(students=self.request.user)

        return context


class StudentCourseView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = 'student/course_view.html'

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course

    def get_lesson(self):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = cache.get(f'lesson-{lesson_id}')
        if lesson:
            return lesson
        else:
            lesson = Lesson.objects.filter(id=lesson_id).first()
            cache.set(f'lesson-{lesson_id}', lesson)
            return lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        context['course'] = course
        context['modules'] = course.modules.all()
        context['current_lesson'] = self.get_lesson()
        return context


def select_lesson_view(request, lesson_id):
    lesson = cache.get(f'lesson-{lesson_id}')
    if not lesson:
        lesson = Lesson.objects.filter(id=lesson_id).first()
        cache.set(f'lesson-{lesson_id}', lesson)
    return render(request, 'hx/lesson/video.html', context={'current_lesson': lesson})


def lesson_note_view(request, content_id):
    item = Content.objects.get(id=content_id).item
    return render(request, 'hx/modal.html', context={'content': item.content, 'title': 'Notas'})


def course_search_view(request, course_id):
    course = cache.get(f'course-{course_id}')
    if not course:
        course = Course.objects.filter(id=course_id).first()
        cache.set(f'course-{course_id}', course)
    return render(request, 'hx/course/search.html', context={'course': course})


def course_content_search_view(request, course_id):
    course = cache.get(f'course-{course_id}')
    if not course:
        course = Course.objects.filter(id=course_id).first()
        cache.set(f'course-{course_id}', course)

    search = request.POST.get('search')

    if search == "":
        return HttpResponse("<h5>Iniciar uma nova pesquisa</h5> <p>Para encontrar aulas deste curso.</p>")

    lessons = Lesson.objects.filter(course=course, title__icontains=search).all()

    if not lessons.exists():
        return HttpResponse("<h5>Não foi encontrado nenhum resultado para sua busca</h5>")

    return render(request, 'hx/course/search_content.html', context={'lessons': lessons, 'search': search})


@csrf_exempt
def course_update_current_lesson(request, course_id):
    lesson_id = json.loads(request.body)['lesson_id']
    CourseRelation.objects.filter(course__id=course_id, user=request.user).update(current_lesson=lesson_id)
    return JsonResponse({'saved': 'ok'})
