import pytest

from selenium.webdriver.common.by import By

from tests.base import TestCourseLessonBase


@pytest.mark.functional_test
@pytest.mark.django_db
class TestCourseOverview(TestCourseLessonBase):

    def test_user_can_view_overview(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        search = self.browser.find_element(By.ID, 'overview')
        search.click()

        self.assertIn(
            'Sobre este curso',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
