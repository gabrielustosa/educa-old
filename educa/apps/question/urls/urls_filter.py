from django.urls import path

from educa.apps.question.views import views_filter

app_name = 'question_filter'

urlpatterns = [
    path('i_ask/<int:course_id>/', views_filter.FilterQuestionIAsk.as_view(), name='i_ask'),
    path('all_questions/<int:course_id>/', views_filter.course_all_questions_view, name='all_questions'),
    path('more_answers/<int:course_id>/', views_filter.FilterQuestionMoreAnswers.as_view(), name='more_answers'),
    path('more_recent/<int:course_id>/', views_filter.FilterQuestionMoreRecent.as_view(), name='more_recent'),
    path('without_answer/<int:course_id>/', views_filter.FilterQuestionWithoutAnswer.as_view(), name='without_answer'),
    path('lesson/<int:lesson_id>/', views_filter.FilterQuestionLesson.as_view(), name='lesson'),
]
