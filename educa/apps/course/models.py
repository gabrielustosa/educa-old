from django.db import models
from django.db.models import Avg, Q
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
    short_description = models.TextField()
    learn_description = models.TextField()
    requirements = models.TextField()
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

    def get_rating_avg(self):
        result = self.ratings.aggregate(Avg('rating'))
        result = result['rating__avg']
        if result:
            return "{:.2f}".format(result)
        return 0

    def get_first_lesson(self):
        return self.lesson_set.order_by('order').first()

    def get_total_lessons(self):
        return self.lesson_set.count()

    def get_total_questions(self):
        from educa.apps.question.models import Question
        return Question.objects.filter(lesson__course=self).count()

    def get_total_files_download(self):
        from educa.apps.content.models import Content
        return Content.objects.filter(lesson__course=self).filter(
            Q(content_type__model='file') | Q(content_type__model='image')).count()

    def get_rating_bars(self):
        ratings = self.ratings

        ranting_dict = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        numbers_rating = [1, 2, 3, 4, 5]
        for number in numbers_rating:
            for rating in ratings.all():
                if int(rating.rating) == number:
                    ranting_dict[int(rating.rating)] = ranting_dict.get(int(rating.rating)) + 1

        result = {}

        for k, v in ranting_dict.items():
            try:
                operation = v / len(ratings.all()) * 100
            except ZeroDivisionError:
                operation = 0
            result[k] = "{:.2f}".format(operation)

        return result

    def get_instructs_list(self):
        list_instructors = []
        for instructor in self.instructors.all():
            if instructor != list_instructors[len(list_instructors) - 1]:
                list_instructors.append(f'{instructor.name}, ')
            else:
                list_instructors.append(instructor.name)

        return list_instructors


class CourseRelation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_lesson = models.PositiveSmallIntegerField()
    subriscred_at = models.DateTimeField(auto_now_add=True)
