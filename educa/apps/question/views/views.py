from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Q
from django.forms import modelform_factory
from django.http import HttpResponse
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.question.models import Question
from educa.apps.question.views.views_filter import course_all_questions_view
from educa.utils import get_lesson_id, render_error


class QuestionMixin(
    LoginRequiredMixin,
    TemplateView,
):
    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course

    def get_lesson(self):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = cache.get(f'lesson-{lesson_id}')
        if lesson:
            return lesson
        else:
            lesson = Lesson.objects.filter(id=lesson_id).first()
            cache.set(f'lesson-{lesson_id}', lesson)
            return lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lesson_id'] = get_lesson_id(self.request)
        context['course'] = self.get_course()

        return context


class QuestionView(QuestionMixin):
    template_name = 'hx/question/course/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['questions'] = Question.objects.filter(lesson__course=self.get_course())

        return context


class QuestionRenderCreateView(QuestionMixin):
    template_name = 'hx/question/render/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = modelform_factory(Question, fields=('title', 'content'))

        return context


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

        context['questions'] = Question.objects.filter(lesson__course=self.get_course())

        return self.render_to_response(context)


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
