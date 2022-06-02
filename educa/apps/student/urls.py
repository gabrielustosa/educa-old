from django.urls import path

from .views import views_course
from .views import views_lesson

app_name = 'student'

urlpatterns = [
    path('course/enroll/<int:course_id>/', views_course.CourseEnrollView.as_view(), name='enroll'),
    path('courses/', views_course.StudentCourseListView.as_view(), name='courses'),
    path('course/<slug:course_id>/lesson/<int:lesson_id>/', views_course.StudentCourseView.as_view(), name='view'),
    path('course/lesson/<int:lesson_id>/', views_lesson.SelectLessonView.as_view(), name='select_video'),
    path('course/lesson/note/<int:content_id>/', views_lesson.LessonNoteView.as_view(), name='lesson_note'),
    path('course/search/<int:course_id>/', views_lesson.CourseSearchView.as_view(), name='search'),
    path('course/search/content/<int:course_id>/', views_lesson.CourseLessonSearchView.as_view(), name='content_search'),
    path('course/update_lesson/<int:course_id>/', views_lesson.CourseUpdateCurrentLessonView.as_view(), name='update_lesson'),
]
