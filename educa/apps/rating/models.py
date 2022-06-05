from django.contrib.auth.models import User
from django.db import models

from educa.apps.course.models import Course


class Rating(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='ratings',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(
        verbose_name='Avaliação'
    )
    comment = models.TextField('Comentário')
    answer = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.rating}'
