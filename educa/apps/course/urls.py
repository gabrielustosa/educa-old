from django.urls import path

from .views import views_crud
from .views import views

app_name = 'course'

urlpatterns = [
    path('mine/', views.CourseOwnerListView.as_view(), name='mine'),
    path('detail/<int:course_id>/', views.CourseDetailView.as_view(), name='detail'),
    path('create/', views_crud.CourseCreateView.as_view(), name='create'),
    path('udpdate/<int:course_id>/', views_crud.CourseUpdateView.as_view(), name='update'),
    path('delete/<int:course_id>/', views_crud.CourseDeleteView.as_view(), name='delete'),
    path('search/', views.CourseSearchView.as_view(), name='search'),
    path('modules/<int:course_id>/', views.CourseModulesView.as_view(), name='modules')
]
