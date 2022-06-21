from django.db import models
from django.utils.text import slugify

from educa.apps.student.models import User
from educa.apps.subject.models import Subject


class Course(models.Model):
    instructors = models.ManyToManyField(
        User,
        related_name='courses_created',
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name='Matéria',
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        User,
        related_name='courses_own',
        on_delete=models.CASCADE,
    )
    short_description = models.TextField('Descrição curta')
    learn_description = models.TextField('Descrição de aprendizado')
    requirements = models.TextField('Requirementos para o curso')
    description = models.TextField('Descrição')
    image = models.ImageField('Imagem', upload_to='profiles/')
    created = models.DateField(auto_now_add=True)
    students = models.ManyToManyField(
        User,
        related_name='courses',
        through='CourseRelation',
        blank=True
    )

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_first_lesson(self):
        return self.lesson_set.order_by('order').first()

    def total_files_download(self):
        from educa.apps.content.models import Content
        return Content.objects.filter(lesson__course=self).filter(content_type__model__in=['file', 'image']).count()


class CourseRelation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_lesson = models.PositiveSmallIntegerField()
    subriscred_at = models.DateTimeField(auto_now_add=True)
