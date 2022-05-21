from django.urls import path

from educa.apps.question.views import views_question

app_name = 'question_view'

urlpatterns = [
    path('view/<int:question_id>/', views_question.QuestionView.as_view(), name='view'),
    path('render/update/<int:question_id>/', views_question.QuestionRenderUpdateView.as_view(), name='render_update'),
    path('update/<int:question_id>/', views_question.QuestionUpdateView.as_view(), name='update'),
    path('confirm/<int:question_id>/', views_question.QuestionConfirmDeleteView.as_view(), name='confirm'),
    path('delete/<int:question_id>/', views_question.QuestionDeleteView.as_view(), name='delete'),
]
