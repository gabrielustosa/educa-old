from django.urls import path

from .views import views, views_crud

app_name = 'notice'

urlpatterns = [
    path('view/<int:course_id>/', views.NoticeView.as_view(), name='view'),
    path('render/create/<int:course_id>/', views.NoticeRenderCreateView.as_view(), name='render_create'),
    path('create/<int:course_id>/', views_crud.NoticeCreateView.as_view(), name='create'),
    path('render/update/<int:notice_id>/', views.NoticeRenderUpdateView.as_view(), name='render_update'),
    path('update/<int:notice_id>/', views_crud.NoticeUpdateView.as_view(), name='update'),
    path('confirm/<int:notice_id>/', views.NoticeConfirmView.as_view(), name='confirm'),
    path('delete/<int:notice_id>/', views_crud.NoticeDeleteView.as_view(), name='delete'),
]
