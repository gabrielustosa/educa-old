from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson
from educa.apps.note.models import Note
from educa.utils.mixin import CacheMixin
from educa.utils.utils import render_error


class NoteView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/note/view.html'
    http_method_names = ['post', 'get', 'head', 'options']

    def get_kwargs(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lesson'] = self.get_lesson()
        context['notes'] = Note.objects.filter(user=self.request.user, lesson=self.get_lesson())

        return context


class NoteRenderCreateView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/note/render/create.html'
    http_method_names = ['post', 'get', 'head', 'options']

    def get_kwargs(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lesson'] = self.get_lesson()
        context['form'] = modelform_factory(Note, fields=('note',))

        return context


class NoteCreateView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/note/view.html'

    def get_kwargs(self):
        return self.request.POST

    def post(self, request, *args, **kwargs):
        note = request.POST.get('note')
        time = request.POST.get('time')

        error_messages = []
        if len(note.replace(' ', '')) == 0:
            error_messages.append('A sua observação não pode estar vázia.')

        if len(time) == 0:
            error_messages.append('Você precisa estar na parte do vídeo que você deseja criar a observação.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        Note.objects.create(lesson=self.get_lesson(), user=self.request.user, note=note, time=time)

        return redirect(reverse('note:view') + f'?lesson_id={self.get_lesson().id}')
