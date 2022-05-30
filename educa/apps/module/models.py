from django.db import models

from educa.apps.course.models import Course
from educa.fields import OrderField


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

    def get_total_lessons(self):
        from educa.apps.lesson.models import Lesson
        return Lesson.objects.filter(module=self).count()
