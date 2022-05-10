from django.urls import path

from . import views

app_name = 'course'

urlpatterns = [
    path('mine/', views.CourseOwnerListView.as_view(), name='mine'),
    path('create/', views.CourseCreateView.as_view(), name='create'),
    path('udpdate/<int:pk>/', views.CourseUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.CourseDeleteView.as_view(), name='delete'),
]
