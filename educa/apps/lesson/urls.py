from django.urls import path

from .views import views
from .views import views_manage

app_name = 'lesson'

urlpatterns = [
    path('create/<int:module_id>/', views_manage.LessonCreateView.as_view(), name='create'),
    path('detail/<int:lesson_id>/', views_manage.LessonDetailView.as_view(), name='detail'),
    path('update/<int:lesson_id>/', views_manage.LessonUpdateView.as_view(), name='update'),
    path('delete/<int:lesson_id>/', views_manage.LessonDeleteView.as_view(), name='delete'),
    path('order/<int:module_id>/', views.LessonOrderView.as_view(), name='order'),
]
