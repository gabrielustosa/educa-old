from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return '/'

    def __str__(self):
        return self.title
