from django.db import models
from embed_video.fields import EmbedVideoField

from educa.apps.course.models import Course
from educa.apps.module.fields import OrderField
from educa.apps.module.models import Module


class Lesson(models.Model):
    title = models.CharField('Título', max_length=100)
    video = EmbedVideoField(verbose_name='Vídeo')
    module = models.ForeignKey(
        Module,
        related_name='lessons',
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return self.title
