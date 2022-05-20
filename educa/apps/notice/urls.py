from django.urls import path

from . import views

app_name = 'notice'

urlpatterns = [
    path('view/<int:course_id>/', views.notice_view, name='view'),
    path('render/create/<int:course_id>/', views.notice_render_create_form_view, name='render_create'),
    path('create/<int:course_id>/', views.notice_create_view, name='create'),
    path('render/update/<int:notice_id>/', views.notice_render_update_form_view, name='render_update'),
    path('update/<int:notice_id>/', views.notice_update_view, name='update'),
    path('confirm/<int:notice_id>/', views.notice_confirm_view, name='confirm'),
    path('delete/<int:notice_id>/', views.notice_delete_view, name='delete'),
]
