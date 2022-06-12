from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.content.models import Text


class TextContentForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'height': '400px'}}),
        }
