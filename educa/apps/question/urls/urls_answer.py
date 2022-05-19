from django.urls import path

from educa.apps.question.views import views_answer

app_name = 'answer'

urlpatterns = [
    path('create/<int:question_id>/', views_answer.create_answer_view, name='create'),
    path('update/<int:answer_id>/', views_answer.update_answer_view, name='update'),
    path('save/<int:answer_id>/', views_answer.save_answer_view, name='save'),
]
