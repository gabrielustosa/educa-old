from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('courses/', views.StudentCourseListView.as_view(), name='courses'),
    path('course/view/<int:course_id>/', views.StudentCourseView.as_view(), name='view'),
    path('course/lesson/<int:lesson_id>/', views.select_lesson_view, name='select_video'),
]
