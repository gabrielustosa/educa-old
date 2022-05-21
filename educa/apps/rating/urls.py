from django.urls import path

from . import views

app_name = 'rating'

urlpatterns = [
    path('view/<int:course_id>/', views.rating_view, name='view'),
    path('create/<int:course_id>/', views.rating_create_view, name='create'),
    path('render/create/<int:course_id>/', views.rating_render_create_view, name='render_create'),
]
