from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.utils.mixin import CourseOwnerMixin
from educa.apps.notice.models import Notice


def notice_view(request, course_id):
    course = cache.get(f'course-{course_id}')
    if not course:
        course = Course.objects.filter(id=course_id).first()
        cache.set(f'course-{course_id}', course)
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
