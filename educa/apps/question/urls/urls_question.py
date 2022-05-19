from django.urls import path

from educa.apps.question.views import views_question

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views_question.course_questions_view, name='course'),
    path('create/<int:course_id>/', views_question.question_create_view, name='create'),
    path('ask/<int:lesson_id>/', views_question.question_ask_view, name='ask'),
    path('search/<int:course_id>/', views_question.question_search_view, name='search'),
    path('view/<int:question_id>/', views_question.question_view, name='view'),
]
