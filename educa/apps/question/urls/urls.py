from django.urls import path

from educa.apps.question.views import views

app_name = 'question'

urlpatterns = [
    path('course/<int:course_id>/', views.QuestionAll.as_view(), name='course'),
    path('render/create/<int:course_id>/', views.QuestionRenderCreate.as_view(), name='render_create'),
    path('create/<int:lesson_id>/', views.QuestionCreate.as_view(), name='create'),
    path('search/<int:course_id>/', views.QuestionSearch.as_view(), name='search'),
]
