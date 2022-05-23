import factory

from educa.apps.lesson.models import Lesson
from tests.factories.course import CourseFactory
from tests.factories.module import ModuleFactory


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson
        django_get_or_create = ('title', 'video', 'module', 'course', 'order')

    title = factory.Faker('name')
    video = 'https://www.youtube.com/watch?v=Ejkb_YpuHWs&list=PLHz_AreHm4dkZ9-atkcmcBaMZdmLHft8n&ab_channel=CursoemV%C3%ADdeo'
    module = factory.SubFactory(ModuleFactory)
    course = factory.SubFactory(CourseFactory)
    order = None
