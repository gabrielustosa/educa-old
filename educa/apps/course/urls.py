from django.urls import path

from .views import views_manager
from .views import views

app_name = 'course'

urlpatterns = [
    path('mine/', views.CourseOwnerListView.as_view(), name='mine'),
    path('detail/<int:course_id>/', views.CourseDetailView.as_view(), name='detail'),

    path('create/', views_manager.CourseCreateView.as_view(), name='create'),
    path('udpdate/<int:pk>/', views_manager.CourseUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views_manager.CourseDeleteView.as_view(), name='delete'),
]
