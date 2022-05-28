from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.mixin import CourseOwnerMixin
from educa.apps.notice.models import Notice
from educa.apps.notice.views.views import notice_view
from educa.utils import render_error


class NoticeCreateView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    http_method_names = ['post']

    def get_course(self):
        return get_object_or_404(Course, id=self.kwargs.get('course_id'))

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')

        error_messages = []
        if len(title) <= 5:
            error_messages.append('O título deve conter mais que 5 carácteres.')

        if len(content) == 0:
            error_messages.append('Os detalhes do seu aviso não podem estar vazios.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        Notice.objects.create(course=self.get_course(), title=title, content=content)

        return notice_view(request, self.kwargs.get('course_id'))


class NoticeUpdateView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    http_method_names = ['post']

    @cached_property
    def get_notice(self):
        return get_object_or_404(Notice, id=self.kwargs.get('notice_id'))

    def get_course(self):
        return self.get_notice.course

    def post(self, request, *args, **kwargs):
        notice = self.get_notice

        title = request.POST.get('title')
        content = request.POST.get('content')

        error_messages = []
        if len(title) <= 5:
            error_messages.append('O título deve conter mais que 5 carácteres.')

        if len(content) == 0:
            error_messages.append('Os detalhes do seu aviso não podem estar vazios.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        notice.title = title
        notice.content = content
        notice.save()

        return notice_view(request, notice.course.id)


class NoticeDeleteView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    @cached_property
    def get_notice(self):
        return get_object_or_404(Notice, id=self.kwargs.get('notice_id'))

    def get_course(self):
        return self.get_notice.course

    def post(self, request, *args, **kwargs):
        notice = self.get_notice

        notice.delete()

        return notice_view(request, notice.course.id)
