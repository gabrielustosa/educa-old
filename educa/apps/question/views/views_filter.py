from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.question.models import Question


def course_all_questions_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__module__course=course)
    return render(request, 'hx/question/course/course_all_questions.html',
                  context={'questions': questions, 'course': course})


def lesson_questions_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'hx/question/lesson/lesson_questions.html',
                  context={'lesson': lesson, 'questions': lesson.questions.all()})


def question_i_ask_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__module__course=course, user=request.user)
    return render(request, 'hx/question/filter/question_i_did.html',
                  context={'questions': questions, 'course': course})


def question_more_answers_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects. \
        filter(lesson__module__course=course). \
        annotate(total=Count('answers')). \
        order_by('-total')
    return render(request, 'hx/question/filter/question_more_answers.html',
                  context={'questions': questions, 'course': course})


def question_more_recent_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__module__course=course).order_by('-updated')
    return render(request, 'hx/question/filter/question_more_recent.html',
                  context={'questions': questions, 'course': course})


def question_without_answer_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects. \
        filter(lesson__module__course=course). \
        annotate(total=Count('answers')). \
        filter(total__exact=0)
    return render(request, 'hx/question/filter/question_without_answer.html',
                  context={'questions': questions, 'course': course})
