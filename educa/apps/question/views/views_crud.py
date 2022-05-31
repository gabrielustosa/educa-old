from django.http import HttpResponse

from educa.utils.mixin import QuestionOwnerMixin, QuestionViewMixin, QuestionMixin
from educa.apps.question.models import Question
from educa.apps.question.views.views_filter import course_all_questions_view
from educa.utils.utils import render_error


class QuestionCreateView(QuestionMixin):
    template_name = 'hx/question/course/questions.html'
    http_method_names = ['post']

    def get_course(self):
        return self.get_lesson().course

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

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

        context['context_object'] = Question.objects.filter(lesson__course=self.get_course())

        return self.render_to_response(context)


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
        self.get_question.delete()

        return course_all_questions_view(request, self.get_question.lesson.course.id)
