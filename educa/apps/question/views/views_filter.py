from django.db.models import Count
from django.urls import reverse

from educa.apps.question.models import Question
from educa.utils.mixin.question import FilterQuestionMixin


class FilterQuestionAll(FilterQuestionMixin):
    template_name = 'hx/question/filter/all_questions.html'

    def get_absolute_url(self):
        return reverse('question_filter:all_questions', kwargs={'course_id': self.get_course().id})

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course())


class FilterQuestionLesson(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_lesson.html'

    def get_kwargs(self):
        return self.request.GET

    def get_absolute_url(self):
        return reverse('question_filter:lesson', kwargs={'lesson_id': self.get_lesson().id})

    def get_queryset(self):
        return self.get_lesson().questions.all()


class FilterQuestionIAsk(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_i_did.html'

    def get_absolute_url(self):
        return reverse('question_filter:i_ask', kwargs={'course_id': self.get_course().id})

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course(), user=self.request.user)


class FilterQuestionMostAnswered(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_most_answers.html'

    def get_absolute_url(self):
        return reverse('question_filter:most_answered', kwargs={'course_id': self.get_course().id})

    def get_queryset(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('answers')). \
            order_by('-total')


class FilterQuestionMostRecent(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_most_recent.html'

    def get_absolute_url(self):
        return reverse('question_filter:most_recent', kwargs={'course_id': self.get_course().id})

    def get_queryset(self):
        return Question.objects.filter(lesson__course=self.get_course()).order_by('updated')


class FilterQuestionWithoutAnswer(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_without_answer.html'

    def get_absolute_url(self):
        return reverse('question_filter:without_answer', kwargs={'course_id': self.get_course().id})

    def get_queryset(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('answers')). \
            filter(total__exact=0)


class FilterQuestionMostVoted(FilterQuestionMixin):
    template_name = 'hx/question/filter/question_most_voted.html'

    def get_absolute_url(self):
        return reverse('question_filter:without_answer', kwargs={'course_id': self.get_course().id})

    def get_queryset(self):
        return Question.objects. \
            filter(lesson__course=self.get_course()). \
            annotate(total=Count('user_likes')). \
            order_by('-total')
