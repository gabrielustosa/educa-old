from django.urls import path

from . import views

app_name = 'content'

urlpatterns = [
    path(
        'create/<int:module_id>/content/<model_name>/',
        views.ContentCreateUpdateView.as_view(),
        name='create'
    ),
    path(
        'update/<int:module_id>/content/<model_name>/<int:object_id>/',
        views.ContentCreateUpdateView.as_view(),
        name='update'
    ),
    path(
        'delete/<int:pk>/',
        views.ContentDeleteView.as_view(),
        name='delete',
    )
]
