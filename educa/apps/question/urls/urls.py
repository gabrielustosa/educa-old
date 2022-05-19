from django.urls import path

from educa.apps.question.views import views

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views.course_questions_view, name='course'),
    path('create/<int:course_id>/', views.question_create_view, name='create'),
    path('ask/<int:lesson_id>/', views.question_ask_view, name='ask'),
    path('search/<int:course_id>/', views.question_search_view, name='search'),
    path('view/<int:question_id>/', views.question_view, name='view'),
]
