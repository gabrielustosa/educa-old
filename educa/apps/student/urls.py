from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('courses/', views.StudentCourseListView.as_view(), name='courses'),
    path('course/<slug:course_slug>/lesson/<int:lesson_id>/', views.student_course_view, name='view'),
    path('course/lesson/<int:lesson_id>/', views.select_lesson_view, name='select_video'),
    path('course/lesson/note/<int:content_id>/', views.lesson_note_view, name='lesson_note'),
    path('course/search/<int:course_id>/', views.course_search_view, name='search'),
    path('course/search/content/<int:course_id>/', views.course_content_search_view, name='content_search'),
    path('course/update_lesson/<int:course_id>/', views.course_update_current_lesson, name='update_lesson'),
]
