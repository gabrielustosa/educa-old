import factory
from django.utils.text import slugify

from educa.apps.course.models import Course
from subject import SubjectFactory
from user import UserFactory


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ('owner', 'subject', 'title', 'slug', 'description', 'image', 'created')

    owner = factory.SubFactory(UserFactory)
    subject = factory.SubFactory(SubjectFactory)
    title = factory.Faker('name')
    description = factory.Faker('sentence')
    image = factory.Faker('image_url')
    created = factory.Faker('date')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)
