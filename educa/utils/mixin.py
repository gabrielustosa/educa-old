from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView, ListView

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.module.models import Module
from educa.apps.question.models import Answer, Question
from educa.settings import QUESTION_PAGINATE_BY
from educa.utils.utils import get_lesson_id


class CourseOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        course = self.get_course()
        if course.owner != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class QuestionOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        question = self.get_question
        if question.user != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class CacheMixin:
    def get_kwargs(self):
        return self.kwargs

    def get_lesson(self):
        lesson_id = self.get_kwargs().get('lesson_id')
        lesson = cache.get(f'lesson-{lesson_id}')
        if lesson:
            return lesson
        else:
            lesson = Lesson.objects.filter(id=lesson_id).first()
            cache.set(f'lesson-{lesson_id}', lesson)
            return lesson

    def get_module(self):
        module_id = self.get_kwargs().get('module_id')
        module = cache.get(f'module-{module_id}')
        if module:
            return module
        else:
            module = Module.objects.filter(id=module_id).first()
            cache.set(f'module-{module_id}', module)
            return module

    def get_course(self):
        course_id = self.get_kwargs().get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course


class QuestionMixin(
    LoginRequiredMixin,
    CacheMixin,
):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lesson_id'] = get_lesson_id(self.request)
        context['course'] = self.get_course()

        return context


class AnswerMixin(
    LoginRequiredMixin,
    TemplateView
):

    @cached_property
    def get_answer(self):
        return get_object_or_404(Answer, id=self.kwargs.get('answer_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['answer'] = self.get_answer

        return context


class QuestionViewMixin(
    LoginRequiredMixin,
    TemplateView,
):

    @cached_property
    def get_question(self):
        return get_object_or_404(Question, id=self.kwargs.get('question_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['question'] = self.get_question

        return context


class FilterQuestionMixin(
    LoginRequiredMixin,
    CacheMixin,
    ListView,
):
    model = Question
    paginate_by = QUESTION_PAGINATE_BY
    context_object_name = 'context_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_course():
            context['course'] = self.get_course()
        if self.get_lesson():
            context['lesson'] = self.get_lesson()

        return context
