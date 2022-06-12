from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.note.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']
        widgets = {
            'note': SummernoteWidget(),
        }
