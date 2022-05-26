import factory

from educa.apps.question.models import Answer
from tests.factories.question import QuestionFactory
from tests.factories.user import UserFactory


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
        django_get_or_create = ('user', 'question', 'content')

    user = factory.SubFactory(UserFactory)
    question = factory.SubFactory(QuestionFactory)
    content = factory.Faker('sentence')
