from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from educa.apps.content.models import Content
from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.student.forms import UserCreateForm


class StudentRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('student:list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(user)
        return result


class StudentCourseListView(TemplateView):
    template_name = 'student/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['courses'] = Course.objects.filter(students=self.request.user)

        return context


def student_course_view(request, course_slug, lesson_id):
    context = {}
    course = get_object_or_404(Course, slug=course_slug)
    context['course'] = course
    context['current_lesson'] = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'student/view.html', context=context)


def select_lesson_view(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, 'hx/lesson/lesson_video.html', context={'current_lesson': lesson})


def lesson_note_view(request, content_id):
    item = Content.objects.get(id=content_id).item

    return render(request, 'hx/modal.html', context={'content': item.content, 'title': 'Notas'})
