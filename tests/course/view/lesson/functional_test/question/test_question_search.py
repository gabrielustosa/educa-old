from time import sleep

import pytest

from tests.base import TestCourseLessonBase


@pytest.mark.slow
@pytest.mark.django_db
class TestSearchQuestion(TestCourseLessonBase):
    def test_user_can_search_question(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()
        question = self.create_question(course)[0]

        self.wait_element_to_be_clickable('questions-answers')

        body = self.wait_element_exists('search-question')
        search_box = self.get_by_input_name(body, 'search')
        search_box.send_keys(question.title)

        sleep(1)

        self.assertIn(
            'Resultados para a sua pesquisa (1 resultados)',
            self.wait_element_exists('content').text
        )
