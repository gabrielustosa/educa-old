from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.question.models import Question, Answer
from educa.apps.question.views.views_filter import course_all_questions_view


def course_questions_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__module__course=course)
    lesson_id = request.GET.get('lesson_id') if request.GET.get('lesson_id') else request.POST.get('lesson_id')
    return render(request, 'hx/question/course/questions.html',
                  context={'course': course,
                           'questions': questions,
                           'lesson_id': lesson_id})


def question_create_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = modelform_factory(Question, fields=('title', 'content'))
    lesson_id = request.GET.get('lesson_id') if request.GET.get('lesson_id') else request.POST.get('lesson_id')
    return render(request, 'hx/question/create.html',
                  context={'form': form,
                           'course': course,
                           'lesson_id': lesson_id})


@require_POST
def question_ask_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    title = request.POST.get('title')
    content = request.POST.get('content')

    Question.objects.create(lesson=lesson, user=request.user, title=title, content=content)
    course = lesson.module.course
    questions = Question.objects.filter(lesson__module__course=course)

    return render(request, 'hx/question/course/questions.html',
                  context={'questions': questions,
                           'course': course,
                           'lesson_id': request.POST.get('lesson_id')})


@require_POST
def question_search_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    search = request.POST.get('search')

    if search == "":
        return course_all_questions_view(request, course_id)

    questions = Question.objects.filter(lesson__module__course=course). \
        filter(Q(title__icontains=search) | Q(content__icontains=search))

    return render(request, 'hx/question/search.html',
                  context={'questions': questions,
                           'course': course})


def question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    form = modelform_factory(Answer, fields=('content',))
    return render(request, 'hx/question/view.html',
                  context={'question': question,
                           'answers': answers,
                           'form': form})


def question_update_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    form = modelform_factory(Question, fields=('title', 'content'))
    form = form(instance=question)
    return render(request, 'hx/question/update.html',
                  context={'form': form,
                           'question': question})


def question_save_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    question.title = request.POST.get('title')
    question.content = request.POST.get('content')
    question.save()

    return render(request, 'hx/question/content.html',
                  context={'question': question})


def question_confirm_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    return render(request, 'hx/modal.html',
                  context={'title': 'Confirmação',
                           'content': 'Você tem certeza que deseja deletar sua pergunta?',
                           'confirm': True,
                           'question': question})


def question_delete_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    question.delete()

    return course_all_questions_view(request, question.lesson.module.course.id)
