from time import sleep

import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from educa.apps.course.models import CourseRelation
from tests.base import FunctionalTestBase, CourseLessonMixin
from tests.factories.user import UserFactory


@pytest.mark.functional_test
class TestFunctionalCourseSearch(CourseLessonMixin, FunctionalTestBase):

    def test_user_can_search(self):
        course = self.course
        self.browser.get(self.live_server_url + reverse('student:view',
                                                        kwargs={'course_slug': course.slug,
                                                                'lesson_id': self.get_lesson_by_id(1).id}))
        username = 'tester'
        password = 'tester'
        user = UserFactory(username=username, password=password)
        CourseRelation.objects.create(course=course, user=user, current_lesson=1)
        self.login(user=user, is_superuser=True, username=username, password=password)

        search = self.get_element_by_id('search')
        search.click()

        body = self.browser.find_element(By.TAG_NAME, 'body')
        search_box = self.get_by_input_name(body, 'search')
        search_box.send_keys('title-4')

        self.assertIn(
            'title-4',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
