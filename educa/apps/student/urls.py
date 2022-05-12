from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('courses', views.StudentCoursesView.as_view(), name='courses'),
]
