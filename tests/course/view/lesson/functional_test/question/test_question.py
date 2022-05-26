import pytest

from selenium.webdriver.common.by import By

from tests.base import TestCourseLessonBase


@pytest.mark.slow
@pytest.mark.django_db
class TestAskQuestion(TestCourseLessonBase):

    def test_user_can_ask_question(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('ask-button')

        body = self.browser.find_element(By.TAG_NAME, 'body')

        title = 'This is a test title.'
        title_input = self.get_by_input_name(body, 'title')
        title_input.send_keys(title)

        content = 'This is a test content.'
        content_input = self.get_by_textarea_name(body, 'content')
        content_input.send_keys(content)

        self.wait_element_to_be_clickable('ask')

        self.assertIn(
            'This is a test title.',
            self.wait_element_exists('content').text
        )
        self.assertIn(
            'This is a test content.',
            self.wait_element_exists('content').text
        )


@pytest.mark.slow
@pytest.mark.django_db
class TestViewQuestion(TestCourseLessonBase):

    def test_user_can_view_a_question(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.create_question(course)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('view-question')

        self.assertIn(
            '0 Respostas',
            self.wait_element_exists('content').text
        )


@pytest.mark.slow
@pytest.mark.django_db
class TestUpdateDeleteQuestion(TestCourseLessonBase):

    def test_user_can_update_question(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.create_question(course)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('view-question')

        self.wait_element_to_be_clickable('options')

        self.wait_element_to_be_clickable('edit-question')

        body = self.browser.find_element(By.TAG_NAME, 'body')

        title = 'This is a test substitute title.'
        title_input = self.get_by_input_name(body, 'title')
        title_input.clear()
        title_input.send_keys(title)

        content = 'This is a test substitute content.'
        content_input = self.get_by_textarea_name(body, 'content')
        content_input.clear()
        content_input.send_keys(content)

        self.wait_element_to_be_clickable('save')

        self.assertIn(
            'This is a test substitute title.',
            self.wait_element_exists('content').text
        )
        self.assertIn(
            'This is a test substitute content.',
            self.wait_element_exists('content').text
        )

    def test_user_can_delete_question(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.create_question(course)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable('view-question')

        self.wait_element_to_be_clickable('options')

        self.wait_element_to_be_clickable('delete-question')

        self.wait_element_to_be_clickable('confirm')

        self.assertNotIn(
            'This is a test title.',
            self.wait_element_exists('content').text
        )
