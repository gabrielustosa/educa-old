from django.urls import path

from . import views

app_name = 'subject'

urlpatterns = [
    path('<int:subject_id>/', views.SubjectCourseView.as_view(), name='view'),
]
