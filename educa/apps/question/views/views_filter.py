from django.db.models import Count

from educa.apps.question.models import Question
from educa.utils.mixin import FilterQuestionMixin


class FilterQuestionAll(FilterQuestionMixin):
    template_name = 'hx/question/filter/all_questions.html'

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course())


class FilterQuestionLesson(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_lesson.html'

    def get_queryset(self):
        return self.get_lesson().questions.all()


class FilterQuestionIAsk(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_i_did.html'

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course(), user=self.request.user)


class FilterQuestionMoreAnswers(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_more_answers.html'

    def get_queryset(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('answers')). \
            order_by('-total')


class FilterQuestionMoreRecent(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_more_recent.html'

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course()).order_by('-updated')


class FilterQuestionWithoutAnswer(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_without_answer.html'

    def get_queryset(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('answers')). \
            filter(total__exact=0)
