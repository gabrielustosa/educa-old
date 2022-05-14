from django.urls import path

from . import views

app_name = 'lesson'

urlpatterns = [
    path('order/<int:module_id>/', views.lesson_order_view, name='order'),
    path('create/<int:module_id>/', views.LessonCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.LessonDeleteView.as_view(), name='delete'),
    path('detail/<int:lesson_id>/', views.LessonDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.LessonUpdateView.as_view(), name='update'),
]
