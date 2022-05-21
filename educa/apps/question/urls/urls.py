from django.urls import path

from educa.apps.question.views import views

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views.QuestionView.as_view(), name='course'),
    path('render/create/<int:course_id>/', views.QuestionRenderCreateView.as_view(), name='render_create'),
    path('create/<int:lesson_id>/', views.QuestionCreateView.as_view(), name='create'),
    path('search/<int:course_id>/', views.QuestionSearchView.as_view(), name='search'),
]
