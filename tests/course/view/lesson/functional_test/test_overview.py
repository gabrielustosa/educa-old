import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.base import FunctionalTestBase, CourseLessonMixin


@pytest.mark.functional_test
@pytest.mark.django_db
class TestFunctionalCourseOverview(FunctionalTestBase, CourseLessonMixin):

    def test_user_can_view_overview(self):
        course = self.load_course()
        self.browser.get(self.live_server_url + reverse('student:view',
                                                        kwargs={'course_slug': course.slug,
                                                                'lesson_id': course.get_first_lesson_id()}))
        self.login(is_superuser=True, username='tester', password='tester')

        search = self.get_element_by_id('overview')
        search.click()

        self.assertIn(
            'Sobre este curso',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
