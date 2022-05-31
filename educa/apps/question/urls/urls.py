from django.urls import path

from educa.apps.question.views import views

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views.QuestionListView.as_view(), name='course'),
    path('render/create/<int:course_id>/', views.QuestionRenderCreateView.as_view(), name='render_create'),
    path('view/<int:question_id>/', views.QuestionView.as_view(), name='view'),
    path('render/update/<int:question_id>/', views.QuestionRenderUpdateView.as_view(), name='render_update'),
    path('confirm/<int:question_id>/', views.QuestionConfirmDeleteView.as_view(), name='confirm_delete'),
    path('search/<int:course_id>/', views.QuestionSearchView.as_view(), name='search'),
]
