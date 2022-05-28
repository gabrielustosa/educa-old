from django.urls import path

from .views import views_crud
from .views import views

app_name = 'course'

urlpatterns = [
    path('mine/', views.CourseOwnerListView.as_view(), name='mine'),
    path('detail/<int:course_id>/', views.CourseDetailView.as_view(), name='detail'),
    path('enrroll/<int:course_id>/', views.course_enrroll_view, name='enrroll'),
    path('create/', views_crud.CourseCreateView.as_view(), name='create'),
    path('udpdate/<int:course_id>/', views_crud.CourseUpdateView.as_view(), name='update'),
    path('delete/<int:course_id>/', views_crud.CourseDeleteView.as_view(), name='delete'),
    path('overview/<int:course_id>/', views_crud.get_course_overview, name='overview'),
]
