from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.functional import cached_property
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.mixin import CourseOwnerMixin
from educa.apps.notice.models import Notice
from educa.utils import render_error


def notice_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    notices = Notice.objects.filter(course=course)
    return render(request, 'hx/notice/view.html', context={'notices': notices, 'course': course})


class NoticeRenderCreateView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'hx/notice/render/create.html'

    def get_course(self):
        return get_object_or_404(Course, id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['course'] = self.get_course()
        context['form'] = modelform_factory(Notice, fields=('title', 'content'))

        return context


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
            error_messages.append('O título deve conter mais que 5 carácteres')

        if len(content) == 0:
            error_messages.append('Os detalhes do seu aviso não podem estar vazios.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        Notice.objects.create(course=self.get_course(), title=title, content=content)

        return notice_view(request, self.kwargs.get('course_id'))


class NoticeRenderUpdateView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'hx/notice/render/update.html'

    @cached_property
    def get_notice(self):
        return get_object_or_404(Notice, id=self.kwargs.get('notice_id'))

    def get_course(self):
        return self.get_notice.course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        notice = self.get_notice
        form = modelform_factory(Notice, fields=('title', 'content'))
        context['form'] = form(instance=notice)
        context['notice'] = notice

        return context


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
            error_messages.append('O título deve conter mais que 5 carácteres')

        if len(content) == 0:
            error_messages.append('Os detalhes do seu aviso não podem estar vazios.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        notice.title = title
        notice.content = content
        notice.save()

        return notice_view(request, notice.course.id)


class NoticeConfirmView(
    LoginRequiredMixin,
    CourseOwnerMixin,
    TemplateView,
):
    template_name = 'hx/modal.html'

    @cached_property
    def get_notice(self):
        return get_object_or_404(Notice, id=self.kwargs.get('notice_id'))

    def get_course(self):
        return self.get_notice.course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        notice = self.get_notice

        context.update({'title': 'Confirmação',
                        'content': 'Você tem certeza que deseja deletar seu aviso?',
                        'confirm': True,
                        'notice': notice})

        return context


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
