import factory

from educa.apps.question.models import Question
from tests.factories.lesson import LessonFactory
from tests.factories.user import UserFactory


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
        django_get_or_create = ('user', 'lesson', 'title', 'content')

    user = factory.SubFactory(UserFactory)
    lesson = factory.SubFactory(LessonFactory)
    title = factory.Faker('name')
    content = factory.Faker('sentence')
