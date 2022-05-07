from django.urls import path

from . import views

app_name = 'content'

urlpatterns = [
    path('create/<int:module_id>/', views.ContentCreateView.as_view(), name='create'),
]
