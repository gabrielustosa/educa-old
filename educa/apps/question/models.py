from django.contrib.auth.models import User
from django.db import models

from educa.apps.lesson.models import Lesson


class Question(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name='questions',
        on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=255)
    content = models.TextField('Detalhes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    content = models.TextField('Resposta')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
