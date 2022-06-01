from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from educa.utils.mixin import QuestionOwnerMixin, QuestionViewMixin, QuestionMixin
from educa.apps.question.models import Question
from educa.utils.utils import render_error


class QuestionCreateView(QuestionMixin, TemplateView):
    http_method_names = ['post']

    def get_course(self):
        return self.get_lesson().course

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')

        error_messages = []
        if len(title) <= 5:
            error_messages.append('O título deve conter mais que 5 carácteres.')

        if len(content) == 0:
            error_messages.append('Os detalhes da sua pergunta não podem estar vazios.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        Question.objects.create(lesson=self.get_lesson(), user=request.user, title=title, content=content)

        return redirect(reverse('question:course',
                                kwargs={
                                    'course_id': self.get_lesson().course_id}) + f'?lesson_id={self.get_lesson().id}')


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


class QuestionDeleteView(QuestionViewMixin):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        question = self.get_question

        self.get_question.delete()

        return redirect(reverse('question_filter:all_questions', kwargs={'course_id': question.lesson.course.id}))
