from django.urls import path

from educa.apps.question.views import views_answer

app_name = 'answer'

urlpatterns = [
    path('create/<int:question_id>/', views_answer.AnswerCreateView.as_view(), name='create'),
    path('render/update/<int:answer_id>/', views_answer.AnswerRenderUpdateView.as_view(), name='render_update'),
    path('update/<int:answer_id>/', views_answer.AnswerUpdateView.as_view(), name='update'),
    path('confirm/<int:answer_id>/', views_answer.AnswerConfirmDeleteView.as_view(), name='confirm'),
    path('delete/<int:answer_id>/', views_answer.AnswerDeleteView.as_view(), name='delete'),
]
