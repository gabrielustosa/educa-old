import factory

from educa.apps.student.models import User
from faker import Faker

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', 'name', 'password', 'username')

    email = factory.Faker('email')
    username = factory.Faker('name')
    name = factory.Faker('name')
    password = 'admin123'
