from django.urls import path

from . import views

app_name = 'rating'

urlpatterns = [
    path('create/<int:course_id>/', views.RatingCreateView.as_view(), name='create'),
]
