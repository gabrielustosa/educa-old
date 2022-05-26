import pytest

from selenium.webdriver.common.by import By

from tests.base import TestCourseLessonBase


@pytest.mark.functional_test
@pytest.mark.django_db
class TestCourseSearch(TestCourseLessonBase):

    def test_user_can_search(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.wait_element_to_be_clickable('search')

        body = self.browser.find_element(By.TAG_NAME, 'body')
        search_box = self.get_by_input_name(body, 'search')
        search_box.send_keys('title-4')

        self.assertIn(
            'title-4',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
