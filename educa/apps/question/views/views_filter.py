from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.lesson.models import Lesson
from educa.apps.question.models import Question


def course_all_questions_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__module__course=course)
    return render(request, 'hx/question/course/all_questions.html',
                  context={'questions': questions, 'course': course})


class FilterQuestionMixin(
    LoginRequiredMixin,
    TemplateView,
):
    @cached_property
    def get_course(self):
        return Course.objects.filter(id=self.kwargs.get('course_id')).first()

    @cached_property
    def get_lesson(self):
        return Lesson.objects.filter(id=self.kwargs.get('lesson_id')).first()

    def get_questions(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_course:
            context['course'] = self.get_course
        if self.get_lesson:
            context['lesson'] = self.get_lesson
        if self.get_questions():
            context['questions'] = self.get_questions()

        return context


class FilterQuestionLesson(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_lesson.html'

    def get_questions(self):
        return self.get_lesson.questions.all()


class FilterQuestionIAsk(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_i_did.html'

    def get_questions(self):
        return Question.objects.filter(lesson__module__course=self.get_course, user=self.request.user)


class FilterQuestionMoreAnswers(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_more_answers.html'

    def get_questions(self):
        return Question.objects. \
            filter(lesson__module__course=self.get_course). \
            annotate(total=Count('answers')). \
            order_by('-total')


class FilterQuestionMoreRecent(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_more_recent.html'

    def get_questions(self):
        return Question.objects.filter(lesson__module__course=self.get_course).order_by('-updated')


class FilterQuestionWithoutAnswer(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_without_answer.html'

    def get_questions(self):
        return Question.objects. \
            filter(lesson__module__course=self.get_course). \
            annotate(total=Count('answers')). \
            filter(total__exact=0)
