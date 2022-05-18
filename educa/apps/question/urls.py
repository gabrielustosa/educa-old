from django.urls import path

from . import views

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views.course_questions_view, name='course'),
    path('course_all/<int:course_id>/', views.course_all_questions_view, name='course_all'),
    path('lesson/<int:lesson_id>/', views.lesson_questions_view, name='lesson'),
    path('i_ask/<int:course_id>/', views.question_i_ask_view, name='i_ask'),
    path('more_answers/<int:course_id>/', views.question_more_answers_view, name='more_answers'),
    path('more_recent/<int:course_id>/', views.question_more_recent_view, name='more_recent'),
    path('without_answer/<int:course_id>/', views.question_without_answer_view, name='without_answer'),
    path('create/<int:course_id>/', views.question_create_view, name='create'),
    path('ask/<int:lesson_id>/', views.question_ask_view, name='ask'),
]
