from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from educa.apps.lesson.models import Lesson
from educa.apps.module.fields import OrderField


class Content(models.Model):
    lesson = models.ForeignKey(
        Lesson,
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
    order = OrderField(blank=True, for_fields=['lesson'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField(verbose_name='Conteúdo')

    class Meta:
        verbose_name = 'Texto'


class File(ItemBase):
    file = models.FileField(verbose_name='Arquivo', upload_to='files')

    class Meta:
        verbose_name = 'Arquivo'


class Image(ItemBase):
    image = models.ImageField(verbose_name='Imagem', upload_to='images')

    class Meta:
        verbose_name = 'Imagem'


class Link(ItemBase):
    url = models.URLField(verbose_name='Link')

    class Meta:
        verbose_name = 'Link'
