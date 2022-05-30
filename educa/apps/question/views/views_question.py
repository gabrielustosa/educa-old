from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.utils.mixin import QuestionOwnerMixin
from educa.apps.question.models import Question, Answer
from educa.apps.question.views.views_filter import course_all_questions_view
from educa.utils.utils import render_error


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


class QuestionView(QuestionViewMixin):
    template_name = 'hx/question/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['answers'] = self.get_question.answers.all()
        context['form'] = modelform_factory(Answer, fields=('content',))

        return context


class QuestionRenderUpdateView(QuestionViewMixin, QuestionOwnerMixin):
    template_name = 'hx/question/render/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = modelform_factory(Question, fields=('title', 'content'))
        context['form'] = form(instance=self.get_question)

        return context


class QuestionUpdateView(QuestionOwnerMixin, QuestionViewMixin):
    template_name = 'hx/question/content.html'
    http_method_names = ['post']

    def get_current_question(self):
        return self.get_question

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        question = self.get_question

        title = request.POST.get('title')
        content = request.POST.get('content')

        error_messages = []
        if len(title) <= 5:
            error_messages.append('O título deve conter mais que 5 carácteres.')

        if len(content) == 0:
            error_messages.append('Os detalhes da sua pergunta não podem estar vazios.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        question.title = title
        question.content = content
        question.save()

        return self.render_to_response(context)


class QuestionConfirmDeleteView(QuestionViewMixin):
    template_name = 'hx/modal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {'title': 'Confirmação',
                             'content': 'Você tem certeza que deseja deletar sua pergunta?',
                             'confirm': True}
        return context


class QuestionDeleteView(QuestionViewMixin):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.get_question.delete()

        return course_all_questions_view(request, self.get_question.lesson.course.id)
