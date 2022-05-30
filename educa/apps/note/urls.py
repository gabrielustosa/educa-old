from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [
    path('view/', views.NoteView.as_view(), name='view'),
    path('render/create/', views.NoteRenderCreateView.as_view(), name='render_create'),
    path('create/', views.NoteCreateView.as_view(), name='create'),
]
