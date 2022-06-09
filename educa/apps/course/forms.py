from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Row, Column
from django import forms
from django_summernote.widgets import SummernoteWidget

from educa.apps.course.models import Course


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'subject', 'learn_description', 'short_description',
            'requirements', 'description', 'image'
        ]
        widgets = {
            'learn_description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
            'short_description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
            'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
            'requirements': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'subject',
            Field('image',
                  css_class='form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white '
                            'bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 '
                            'focus:text-gray-700 focus:bg-white focus:outline-none', placeholder='Escolha um arquivo'),
            'learn_description',
            'requirements',
            'description',
            'short_description',
            Submit('submit', 'Salvar',
                   css_class="bg-violet-700 px-4 cursor-pointer py-2 my-3 w-full rounded-sm text-white")
        )


class InstructorAddForm(forms.Form):
    instructor = forms.EmailField(label='Novo instrutor', widget=forms.TextInput(attrs={'type': 'email',
                                                                                        'placeholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('instructor'),
                Column(Submit('submit', 'Adicionar',
                              css_class="bg-violet-700 px-4 cursor-pointer ml-3 mt-7 py-2.5 w-full rounded-lg text-white"))
            )
        )
