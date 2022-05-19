from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.question.models import Question, Answer


def course_questions_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__module__course=course)
    return render(request, 'hx/question/course/course_questions.html',
                  context={'course': course, 'questions': questions})


def question_create_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = modelform_factory(Question, fields=('title', 'content'))
    return render(request, 'hx/question/create.html',
                  context={'course': course, 'form': form})


@require_POST
def question_ask_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    title = request.POST.get('title')
    content = request.POST.get('content')

    Question.objects.create(lesson=lesson, user=request.user, title=title, content=content)
    course = lesson.module.course
    questions = Question.objects.filter(lesson__module__course=course)

    return render(request, 'hx/question/course/course_all_questions.html',
                  context={'questions': questions, 'course': course})


@require_POST
def question_search_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    search = request.POST.get('search')

    questions = Question.objects.filter(lesson__module__course=course). \
        filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(request, 'hx/question/search.html',
                  context={'questions': questions, 'course': course})


def question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    return render(request, 'hx/question/view.html',
                  context={'question': question, 'answers': answers})
