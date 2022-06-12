from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.notice.models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'height': '400px'}}),
        }
