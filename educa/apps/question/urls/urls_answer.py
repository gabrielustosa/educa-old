from django.urls import path

from educa.apps.question.views import views

app_name = 'answer'

urlpatterns = [
    path('create/<int:question_id>/', views.create_answer_view, name='create'),
]
