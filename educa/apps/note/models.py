from django.contrib.auth.models import User
from django.db import models

from educa.apps.lesson.models import Lesson


class Note(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notes',
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )
    time = models.CharField(max_length=10)
    note = models.TextField('Nota')

    def __str__(self):
        return f'{self.id}. {self.lesson} - {self.user}'
