from django.urls import path

from . import views

app_name = 'rating'

urlpatterns = [
    path('view/<int:course_id>/', views.rating_view, name='view'),
    path('render/create/<int:course_id>/', views.RatingRenderCreateView.as_view(), name='render_create'),
    path('create/<int:course_id>/', views.RatingCreateView.as_view(), name='create'),
]
