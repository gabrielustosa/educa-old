import factory

from educa.apps.notice.models import Notice
from tests.factories.course import CourseFactory
from tests.factories.question import QuestionFactory


class NoticeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notice
        django_get_or_create = ('course', 'title', 'content')

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker('name')
    content = factory.Faker('sentence')
