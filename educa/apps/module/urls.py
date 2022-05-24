from django.urls import path

from . import views

app_name = 'module'

urlpatterns = [
    path('create/<int:course_id>/', views.CourseCreateView.as_view(), name='create'),
    path('detail/<int:module_id>/', views.CourseDetailView.as_view(), name='detail'),
    path('update/<int:module_id>/', views.CourseUpdateView.as_view(), name='update'),
    path('delete/<int:module_id>/', views.CourseDeleteView.as_view(), name='delete'),
    path('order/<int:course_id>/', views.module_order_view, name='order'),
]
