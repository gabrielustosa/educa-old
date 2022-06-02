from django.urls import path

from educa.apps.question.views import views_filter

app_name = 'question_filter'

urlpatterns = [
    path('i_ask/<int:course_id>/', views_filter.FilterQuestionIAsk.as_view(), name='i_ask'),
    path('all_questions/<int:course_id>/', views_filter.FilterQuestionAll.as_view(), name='all_questions'),
    path('most_answered/<int:course_id>/', views_filter.FilterQuestionMostAnswered.as_view(), name='most_answered'),
    path('most_recent/<int:course_id>/', views_filter.FilterQuestionMostRecent.as_view(), name='most_recent'),
    path('without_answer/<int:course_id>/', views_filter.FilterQuestionWithoutAnswer.as_view(), name='without_answer'),
    path('most_voted/<int:course_id>/', views_filter.FilterQuestionMostVoted.as_view(), name='most_voted'),
    path('lesson/<int:lesson_id>/', views_filter.FilterQuestionLesson.as_view(), name='lesson'),
]
