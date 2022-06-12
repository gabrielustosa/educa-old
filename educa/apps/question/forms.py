from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.question.models import Answer, Question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', ]
        widgets = {
            'content': SummernoteWidget(),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
