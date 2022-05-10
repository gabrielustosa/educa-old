from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from educa.apps.subject.models import Subject


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name='Matéria',
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Descrição')
    image = models.ImageField('Imagem')
    created = models.DateField(auto_now_add=True)
    students = models.ManyToManyField(
        User,
        related_name='courses',
        blank=True
    )

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
