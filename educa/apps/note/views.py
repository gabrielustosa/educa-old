from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from educa.apps.note.models import Note
from educa.mixin import CacheMixin
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

        lesson = self.get_lesson()

        context['context_object'] = Note.objects.filter(user=self.request.user, lesson=lesson)

        self.request.session[f'section-{lesson.course.id}'] = 'note'

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


class NoteRenderUpdateView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/note/render/update.html'

    def get_kwargs(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note = get_object_or_404(Note, id=self.kwargs.get('note_id'))

        context['lesson'] = self.get_lesson()
        form = modelform_factory(Note, fields=('note',))
        context['form'] = form(instance=note)
        context['note'] = note

        return context


class NoteUpdateView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):

    def get_kwargs(self):
        return self.request.GET

    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=self.kwargs.get('note_id'))
        content_note = request.POST.get('note')

        error_messages = []
        if len(content_note) == 0:
            error_messages.append('A sua observação não pode estar vázia.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        note.note = content_note
        note.save()

        return redirect(reverse('note:view') + f'?lesson_id={note.lesson.id}')


class NoteConfirmView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/modal/confirm_body.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        note = get_object_or_404(Note, id=self.kwargs.get('note_id'))

        context.update({'confirm_text': 'Você tem certeza que deseja deletar sua observação?',
                        'post_url': f'/course/note/delete/{note.id}/ ',
                        'target': '#content'})

        return context


class NoteDeleteView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=self.kwargs.get('note_id'))

        note.delete()

        return redirect(reverse('note:view') + f'?lesson_id={note.lesson.id}')
