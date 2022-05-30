from django.db import models

from educa.apps.course.models import Course
from educa.utils.fields import OrderField
from educa.apps.module.models import Module
from educa.utils.utils import get_url_id


class Lesson(models.Model):
    title = models.CharField('Título', max_length=100)
    video = models.URLField(verbose_name='Vídeo')
    video_id = models.CharField(max_length=100, blank=True)
    module = models.ForeignKey(
        Module,
        related_name='lessons',
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['module'])

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not hasattr(self, 'video_id'):
            setattr(self, 'video_id', get_url_id(getattr(self, 'video')))
        return super().save(**kwargs)
