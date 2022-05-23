import factory

from educa.apps.module.models import Module
from tests.factories.course import CourseFactory


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Module
        django_get_or_create = ('course', 'title', 'description', 'order')

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker('name')
    description = factory.Faker('sentence')
    order = None
