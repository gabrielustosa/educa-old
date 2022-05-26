from django.urls import path

from . import views

app_name = 'notice'

urlpatterns = [
    path('view/<int:course_id>/', views.notice_view, name='view'),
    path('render/create/<int:course_id>/', views.NoticeRenderCreateView.as_view(), name='render_create'),
    path('create/<int:course_id>/', views.NoticeCreateView.as_view(), name='create'),
    path('render/update/<int:notice_id>/', views.NoticeRenderUpdateView.as_view(), name='render_update'),
    path('update/<int:notice_id>/', views.NoticeUpdateView.as_view(), name='update'),
    path('confirm/<int:notice_id>/', views.NoticeConfirmView.as_view(), name='confirm'),
    path('delete/<int:notice_id>/', views.NoticeDeleteView.as_view(), name='delete'),
]
