from time import sleep

import pytest

from selenium.webdriver.common.by import By

from tests.base import TestCourseLessonBase


@pytest.mark.slow
@pytest.mark.django_db
class TestAnswerQuestion(TestCourseLessonBase):

    def test_user_can_answer_question(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.create_question(course)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('view-question')

        body = self.wait_element_exists('answers')
        search_box = self.get_by_textarea_name(body, 'content')
        search_box.send_keys('This is a test answer.')

        self.wait_element_to_be_clickable('answer-button')

        self.assertIn(
            'This is a test answer.',
            self.wait_element_exists('content').text
        )

    def test_user_can_update_answer(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        question = self.create_question(course)[0]

        self.create_answer(question)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('view-question')

        self.wait_element_to_be_clickable('option-answer')

        self.wait_element_to_be_clickable('edit-answer')

        body = self.wait_element_exists('answers')

        content = 'This is a test substitute answer content.'
        content_input = self.get_by_textarea_name(body, 'content')
        content_input.clear()
        content_input.send_keys(content)

        self.wait_element_to_be_clickable('save')

        self.assertIn(
            'This is a test substitute answer content.',
            self.wait_element_exists('content').text
        )

    def test_user_can_delete_answer(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        question = self.create_question(course)[0]

        answer = self.create_answer(question)[0]

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('view-question')

        self.wait_element_to_be_clickable('option-answer')

        self.wait_element_to_be_clickable('delete-answer')

        self.wait_element_to_be_clickable('confirm')

        self.assertNotIn(
            answer.content,
            self.wait_element_exists('content').text
        )
