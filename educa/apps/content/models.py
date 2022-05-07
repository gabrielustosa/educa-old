from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from educa.apps.module.fields import OrderField
from educa.apps.module.models import Module


class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': (
            'text',
            'video',
            'image',
            'file')}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()

    class Meta:
        verbose_name = 'Texto'


class File(ItemBase):
    file = models.FileField(upload_to='files')

    class Meta:
        verbose_name = 'Arquivo'


class Image(ItemBase):
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = 'Imagem'


class Video(ItemBase):
    url = models.URLField()

    class Meta:
        verbose_name = 'Vídeo'
