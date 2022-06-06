from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as views_login

from educa.apps.course.views.views import CourseListView
from educa.apps.student.views.views import StudentRegisterView, StudentEditProfileView, StudentProfileView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/register/', StudentRegisterView.as_view(), name='register'),
    path('accounts/login/', views_login.LoginView.as_view(), name='login'),
    path('accounts/logout/', views_login.LogoutView.as_view(), name='logout'),

    path('students/', include('educa.apps.student.urls')),
    path('student/profile/', StudentEditProfileView.as_view(), name='profile'),
    path('student/profile/<int:user_id>/', StudentProfileView.as_view(), name='profile_view'),

    path('course/', include('educa.apps.course.urls')),

    path('module/content/', include('educa.apps.content.urls')),
    path('course/module/', include('educa.apps.module.urls')),

    path('content/lesson/', include('educa.apps.lesson.urls')),

    path('course/rating/', include('educa.apps.rating.urls')),

    path('course/question/', include('educa.apps.question.urls.urls')),
    path('course/question/crud/', include('educa.apps.question.urls.urls_crud')),
    path('course/question/filter/', include('educa.apps.question.urls.urls_filter')),

    path('course/answer/', include('educa.apps.question.urls.urls_answer')),

    path('course/notice/', include('educa.apps.notice.urls')),

    path('course/note/', include('educa.apps.note.urls')),

    path('subject/', include('educa.apps.subject.urls')),

    path('', include('educa.apps.lesson.api.urls')),
    path('', CourseListView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
