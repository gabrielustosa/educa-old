from django.db import models
from django.urls import reverse


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('subject:view', kwargs={'subject_id': self.id})

    def __str__(self):
        return self.title
