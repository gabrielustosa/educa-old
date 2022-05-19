from django.urls import path

from .views import views
from .views import views_filter

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views.course_questions_view, name='course'),
    path('course_all/<int:course_id>/', views_filter.course_all_questions_view, name='course_all'),
    path('lesson/<int:lesson_id>/', views_filter.lesson_questions_view, name='lesson'),
    path('i_ask/<int:course_id>/', views_filter.question_i_ask_view, name='i_ask'),
    path('more_answers/<int:course_id>/', views_filter.question_more_answers_view, name='more_answers'),
    path('more_recent/<int:course_id>/', views_filter.question_more_recent_view, name='more_recent'),
    path('without_answer/<int:course_id>/', views_filter.question_without_answer_view, name='without_answer'),
    path('create/', views.question_create_view, name='create'),
    path('ask/<int:lesson_id>/', views.question_ask_view, name='ask'),
    path('search/<int:course_id>/', views.question_search_view, name='search'),
    path('view/<int:question_id>/', views.question_view, name='view'),
    path('answer/<int:question_id>/', views.create_answer_view, name='answer'),
]
