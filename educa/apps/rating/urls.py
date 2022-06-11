from django.urls import path

from . import views

app_name = 'rating'

urlpatterns = [
    path('view/<int:course_id>/', views.RatingView.as_view(), name='view'),
    path('view/lesson/<int:course_id>/', views.RatingLessonView.as_view(), name='view_lesson'),
    path('render/create/<int:course_id>/', views.RatingRenderCreateView.as_view(), name='render_create'),
    path('create/<int:course_id>/', views.RatingCreateView.as_view(), name='create'),
    path('search/<int:course_id>/', views.RatingSearchView.as_view(), name='search'),
    path('filter/<int:course_id>/', views.RatingFilterView.as_view(), name='filter'),
]
