from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [
    path('view/', views.NoteView.as_view(), name='view'),
    path('render/create/', views.NoteRenderCreateView.as_view(), name='render_create'),
    path('render/update/<int:note_id>/', views.NoteRenderUpdateView.as_view(), name='render_update'),
    path('create/', views.NoteCreateView.as_view(), name='create'),
    path('update/<int:note_id>/', views.NoteUpdateView.as_view(), name='update'),
    path('confirm/<int:note_id>/', views.NoteConfirmView.as_view(), name='confirm'),
    path('delete/<int:note_id>/', views.NoteDeleteView.as_view(), name='delete'),
]
