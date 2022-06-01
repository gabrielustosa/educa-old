from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView, ListView

from educa.apps.question.models import Answer, Question
from educa.settings import QUESTION_PAGINATE_BY
from educa.utils.mixin.course import CacheMixin
from educa.utils.utils import get_lesson_id


class QuestionOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        question = self.get_question
        if question.user != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


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

    def get_absolute_url(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_course():
            context['course'] = self.get_course()
        if self.get_lesson():
            context['lesson'] = self.get_lesson()
        if self.get_absolute_url():
            context['scroll_url'] = self.get_absolute_url()

        if not self.request.GET.get('page'):
            context['first_render'] = True

        return context
