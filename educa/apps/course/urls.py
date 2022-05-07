from django.urls import path

from . import views

app_name = 'course'

urlpatterns = [
    path('mine/', views.CourseOwnerList.as_view(), name='mine'),
    path('create/', views.CourseOwnerCreateView.as_view(), name='create'),
]
