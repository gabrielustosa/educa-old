import pytest

from random import randint

from educa.tests.base import TestCourseLessonBase


@pytest.mark.slow
@pytest.mark.django_db
class TestRating(TestCourseLessonBase):

    def test_user_can_create_notice(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.wait_element_to_be_clickable('rating')

        self.wait_element_to_be_clickable('create-rating-button')

        body = self.wait_element_exists('rating-create')

        rating = randint(1, 5)
        title_input = self.get_by_input_name(body, 'rating')
        title_input.send_keys(rating)

        comment = 'This is a test comment.'
        comment_input = self.get_by_textarea_name(body, 'comment')
        comment_input.send_keys(comment)

        self.wait_element_to_be_clickable('send')

        self.assertIn(
            'This is a test comment.',
            self.wait_element_exists('content').text
        )

    def test_error_message_rating(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        self.wait_element_to_be_clickable('rating')

        self.wait_element_to_be_clickable('create-rating-button')

        body = self.wait_element_exists('rating-create')

        rating = 50
        title_input = self.get_by_input_name(body, 'rating')
        title_input.send_keys(rating)

        comment = ''
        comment_input = self.get_by_textarea_name(body, 'comment')
        comment_input.send_keys(comment)

        self.wait_element_to_be_clickable('send')

        self.assertIn(
            'Você deve escolher um número de 1 a 5.',
            self.wait_element_exists('content').text
        )
        self.assertIn(
            'O comentário da sua avaliação não pode estar vazio.',
            self.wait_element_exists('content').text
        )
