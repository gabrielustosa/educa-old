from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.note.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']
        widgets = {
            'note': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'note',
        )
