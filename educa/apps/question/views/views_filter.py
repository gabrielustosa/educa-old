from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.question.models import Question
from educa.utils.mixin import CacheMixin


def course_all_questions_view(request, course_id):
    course = cache.get(f'course-{course_id}')
    if not course:
        course = Course.objects.filter(id=course_id).first()
        cache.set(f'course-{course_id}', course)
    questions = Question.objects.filter(lesson__course=course)
    return render(request, 'hx/question/filter/all_questions.html',
                  context={'questions': questions, 'course': course})


class FilterQuestionMixin(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):

    def get_questions(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_course():
            context['course'] = self.get_course()
        if self.get_lesson():
            context['lesson'] = self.get_lesson()
        if self.get_questions():
            context['questions'] = self.get_questions()

        return context


class FilterQuestionLesson(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_lesson.html'

    def get_questions(self):
        return self.get_lesson().questions.all()


class FilterQuestionIAsk(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_i_did.html'

    def get_questions(self):
        return Question.objects.filter(lesson__course=self.get_course(), user=self.request.user)


class FilterQuestionMoreAnswers(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_more_answers.html'

    def get_questions(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('answers')). \
            order_by('-total')


class FilterQuestionMoreRecent(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_more_recent.html'

    def get_questions(self):
        return Question.objects.filter(lesson__course=self.get_course()).order_by('-updated')


class FilterQuestionWithoutAnswer(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_without_answer.html'

    def get_questions(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('answers')). \
            filter(total__exact=0)
