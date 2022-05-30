from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from educa.apps.lesson.api.serializer import LessonSerializer
from educa.apps.lesson.models import Lesson


class LessonAPIViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'options', 'head']
