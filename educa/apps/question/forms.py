from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.question.models import Answer, Question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', ]
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '80%', 'height': '400px'}}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'content',
        )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
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
