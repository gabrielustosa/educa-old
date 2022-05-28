from django.urls import path

from .views import views, views_crud

app_name = 'module'

urlpatterns = [
    path('create/<int:course_id>/', views_crud.ModuleCreateView.as_view(), name='create'),
    path('detail/<int:module_id>/', views_crud.ModuleDetailView.as_view(), name='detail'),
    path('update/<int:module_id>/', views_crud.ModuleUpdateView.as_view(), name='update'),
    path('delete/<int:module_id>/', views_crud.ModuleDeleteView.as_view(), name='delete'),
    path('order/<int:course_id>/', views.ModuleOrderView.as_view(), name='order'),
]
