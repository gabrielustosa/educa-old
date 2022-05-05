from django.db import models
from django.contrib.auth.models import User

from educa.apps.subject.models import Subject


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    students = models.ManyToManyField(
        User,
        related_name='courses',
        blank=True
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
