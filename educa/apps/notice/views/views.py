from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.mixin import InstructorRequiredMixin, CacheMixin
from educa.apps.notice.models import Notice


class NoticeView(
    LoginRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/notice/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_course()
        notices = Notice.objects.filter(course=course)
        context['notices'] = notices
        context['course'] = course

        self.request.session[f'section-{course.id}'] = 'notice'

        return context


class NoticeRenderCreateView(
    LoginRequiredMixin,
    InstructorRequiredMixin,
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
    InstructorRequiredMixin,
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
    InstructorRequiredMixin,
    TemplateView,
):
    template_name = 'hx/modal/confirm_body.html'

    @cached_property
    def get_notice(self):
        return get_object_or_404(Notice, id=self.kwargs.get('notice_id'))

    def get_course(self):
        return self.get_notice.course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'confirm_text': 'Você tem certeza que deseja deletar seu alerta?',
                        'post_url': f'/course/notice/delete/{self.get_notice.id}/',
                        'target': '#content'})

        return context
