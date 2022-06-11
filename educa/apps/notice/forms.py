from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.notice.models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'title'
            'content',
        )
