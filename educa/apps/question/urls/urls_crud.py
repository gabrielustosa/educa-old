from django.urls import path

from educa.apps.question.views import views_crud

app_name = 'question_crud'

urlpatterns = [
    path('update/<int:question_id>/', views_crud.QuestionUpdateView.as_view(), name='update'),
    path('delete/<int:question_id>/', views_crud.QuestionDeleteView.as_view(), name='delete'),
    path('create/<int:lesson_id>/', views_crud.QuestionCreateView.as_view(), name='create'),
]
