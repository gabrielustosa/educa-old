from django.db.models import Q
from django.forms import modelform_factory

from educa.apps.question.models import Question, Answer
from educa.apps.question.views.views_crud import QuestionViewMixin
from educa.apps.question.views.views_filter import course_all_questions_view
from educa.utils.mixin import QuestionOwnerMixin, QuestionMixin


class QuestionListView(QuestionMixin):
    template_name = 'hx/question/course/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['questions'] = Question.objects.filter(lesson__course=self.get_course())

        return context


class QuestionView(QuestionViewMixin):
    template_name = 'hx/question/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['answers'] = self.get_question.answers.all()
        context['form'] = modelform_factory(Answer, fields=('content',))

        return context


class QuestionRenderCreateView(QuestionMixin):
    template_name = 'hx/question/render/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = modelform_factory(Question, fields=('title', 'content'))

        return context


class QuestionRenderUpdateView(QuestionViewMixin, QuestionOwnerMixin):
    template_name = 'hx/question/render/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = modelform_factory(Question, fields=('title', 'content'))
        context['form'] = form(instance=self.get_question)

        return context


class QuestionSearchView(QuestionMixin):
    template_name = 'hx/question/search.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        search = request.POST.get('search')

        if search == "":
            return course_all_questions_view(request, self.get_course().id)

        context['questions'] = Question.objects.filter(lesson__course=self.get_course()). \
            filter(Q(title__icontains=search) | Q(content__icontains=search))

        return self.render_to_response(context)


class QuestionConfirmDeleteView(QuestionViewMixin):
    template_name = 'hx/modal_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {
            'confirm_text': 'Você tem certeza que deseja deletar a sua pergunta?',
            'post_url': f'/course/question/crud/delete/{self.get_question.id}/',
            'target': '#question',
        }
        return context
