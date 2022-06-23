import factory

from educa.apps.course.models import Course
from educa.tests.factories.subject import SubjectFactory
from educa.tests.factories.user import UserFactory


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ('owner', 'subject', 'title', 'image', 'created')

    owner = factory.SubFactory(UserFactory)
    subject = factory.SubFactory(SubjectFactory)
    title = factory.Faker('name')
    image = factory.Faker('image_url')
    created = factory.Faker('date')
