from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('courses/', views.StudentCourseListView.as_view(), name='courses'),
    path('course/<slug:course_slug>/lesson/<int:lesson_id>/', views.student_course_view, name='view'),
    path('course/lesson/<int:lesson_id>/', views.select_lesson_view, name='select_video'),
    path('course/lesson/note/<int:content_id>/', views.lesson_note_view, name='lesson_note'),
]
