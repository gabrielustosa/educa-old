import factory
from django.utils.text import slugify

from educa.apps.subject.models import Subject


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
        django_get_or_create = ('title', 'slug')

    title = factory.Faker('name')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)
