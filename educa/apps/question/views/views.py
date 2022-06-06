from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from educa.apps.question.models import Question, Answer
from educa.apps.question.views.views_crud import QuestionViewMixin
from educa.settings import QUESTION_PAGINATE_BY
from educa.mixin.question import QuestionMixin, QuestionOwnerMixin


class QuestionListView(QuestionMixin, ListView):
    template_name = 'hx/question/course/questions.html'
    model = Question
    paginate_by = QUESTION_PAGINATE_BY
    context_object_name = 'context_object'

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.request.session[f'section-{self.get_course().id}'] = 'question'
        course = self.get_course()
        context['course'] = course
        context['scroll_url'] = f'/course/question/filter/all_questions/{course.id}/'

        return context


class QuestionView(QuestionViewMixin):
    template_name = 'hx/question/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['answers'] = self.get_question.answers.all()
        context['form'] = modelform_factory(Answer, fields=('content',))

        return context


class QuestionRenderCreateView(QuestionMixin, TemplateView):
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


class QuestionSearchView(QuestionMixin, TemplateView):
    template_name = 'hx/question/search.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        search = request.POST.get('search')

        if search == "":
            return redirect(reverse('question_filter:all_questions', kwargs={'course_id': self.get_course().id}))

        context['context_object'] = Question.objects.filter(lesson__course=self.get_course()). \
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


class QuestionLikeView(QuestionViewMixin):
    template_name = 'hx/question/likes.html'

    def get(self, request, *args, **kwargs):
        question = self.get_question

        if question.user_likes.filter(id=request.user.id).exists():
            question.user_likes.remove(request.user)
        else:
            question.user_likes.add(request.user)

        return super().get(request, *args, **kwargs)
