"""educa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as views_login

from educa.apps.course.views.views import CourseListView
from educa.apps.student.views import StudentRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', StudentRegisterView.as_view(), name='register'),
    path('accounts/login/', views_login.LoginView.as_view(), name='login'),
    path('accounts/logout/', views_login.LogoutView.as_view(), name='logout'),
    path('students/', include('educa.apps.student.urls')),
    path('course/', include('educa.apps.course.urls')),
    path('module/content/', include('educa.apps.content.urls')),
    path('course/module/', include('educa.apps.module.urls')),
    path('content/lesson/', include('educa.apps.lesson.urls')),
    path('', CourseListView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
