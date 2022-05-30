from rest_framework.routers import SimpleRouter

from educa.apps.lesson.api import view

card_api_v1_router = SimpleRouter()
card_api_v1_router.register(
    'api/v1/lesson',
    view.LessonAPIViewSet
)

urlpatterns = card_api_v1_router.urls
