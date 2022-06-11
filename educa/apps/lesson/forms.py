from django import forms
from django.core.exceptions import ValidationError

from educa.apps.lesson.models import Lesson
from educa.utils.utils import check_video_url


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video']

    def clean_video(self):
        video = self.cleaned_data['video']

        if check_video_url(video):
            raise ValidationError('Você precisa inserir um vídeo do youtube.')

        return video
