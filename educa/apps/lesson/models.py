from django.db import models

from educa.apps.module.fields import OrderField
from educa.apps.module.models import Module


class Lesson(models.Model):
    title = models.CharField('Título', max_length=100)
    video = models.URLField(verbose_name='Vídeo')
    module = models.ForeignKey(
        Module,
        related_name='lessons',
        on_delete=models.CASCADE
    )
    order = OrderField(blank=True, for_fields=['module'])
