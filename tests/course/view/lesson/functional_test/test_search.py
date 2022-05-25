import pytest

from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.base import FunctionalTestBase, CourseLessonMixin


@pytest.mark.functional_test
@pytest.mark.django_db
class TestFunctionalCourseSearch(FunctionalTestBase, CourseLessonMixin):

    def test_user_can_search(self):
        course = self.load_course()
        self.browser.get(self.live_server_url + reverse('student:view',
                                                        kwargs={'course_slug': course.slug,
                                                                'lesson_id': course.get_first_lesson_id()}))

        self.login(is_superuser=True, username='tester', password='tester')

        search = self.get_element_by_id('search')
        search.click()

        body = self.browser.find_element(By.TAG_NAME, 'body')
        search_box = self.get_by_input_name(body, 'search')
        search_box.send_keys('title-4')

        self.assertIn(
            'title-4',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
