from django.urls import path

from . import views

app_name = 'module'

urlpatterns = [
    path('create/<int:course_id>/', views.ModuleCreateView.as_view(), name='create'),
    path('detail/<int:module_id>/', views.ModuleDetailView.as_view(), name='detail'),
]
