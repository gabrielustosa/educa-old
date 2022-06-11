from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from educa.apps.note.forms import NoteForm
from educa.apps.note.models import Note
from educa.mixin import CacheMixin


class NoteView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/note/view.html'

    def get_kwargs(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lesson = self.get_lesson()

        context['notes'] = Note.objects.filter(user=self.request.user, lesson=lesson)
        context['lesson'] = lesson

        self.request.session[f'section-{lesson.course.id}'] = 'note'

        return context


class NoteRenderCreateView(
    LoginRequiredMixin,
    TemplateView,
    CacheMixin,
):
    template_name = 'hx/note/render/create.html'

    def get_kwargs(self):
        return self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lesson'] = self.get_lesson()
        context['form'] = NoteForm()

        return context


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
        context['form'] = NoteForm(instance=note)
        context['note'] = note

        return context


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
