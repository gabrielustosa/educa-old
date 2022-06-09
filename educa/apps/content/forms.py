from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.content.models import Text


class TextContentForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }

    def __init__(self, button_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'content',
            Submit('submit', button_label,
                   css_class="bg-violet-700 px-4 cursor-pointer py-2 my-3 w-full rounded-sm text-white")
        )
