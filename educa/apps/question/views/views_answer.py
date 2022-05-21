from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.question.models import Answer
from educa.apps.question.views.views_question import QuestionViewMixin


class AnswerCreateView(QuestionViewMixin):
    template_name = 'hx/question/answer/answer.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        content = self.request.POST.get('content')
        Answer.objects.create(user=self.request.user, question=self.get_question, content=content)

        context['answers'] = Answer.objects.filter(question=self.get_question)
        context['form'] = modelform_factory(Answer, fields=('content',))

        return self.render_to_response(context)


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


class AnswerRenderUpdateView(AnswerMixin):
    template_name = 'hx/question/answer/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = modelform_factory(Answer, fields=('content',))
        context['form'] = form(instance=self.get_answer)

        return context


class AnswerUpdateView(AnswerMixin):
    template_name = 'hx/question/answer/content.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        answer = self.get_answer
        answer.content = request.POST.get('content')
        answer.save()

        return self.render_to_response(context)


class AnswerConfirmDeleteView(AnswerMixin):
    template_name = 'hx/modal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {'title': 'Confirmação',
                             'content': 'Você tem certeza que deseja deletar sua resposta?',
                             'confirm': True}
        return context


class AnswerDeleteView(AnswerMixin):
    template_name = 'hx/question/answer/answer.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        question = self.get_answer.question
        answers = Answer.objects.filter(question=question)
        form = modelform_factory(Answer, fields=('content',))

        self.get_answer.delete()

        context = {
            'answers': answers,
            'form': form,
            'question': question
        }

        return self.render_to_response(context)
