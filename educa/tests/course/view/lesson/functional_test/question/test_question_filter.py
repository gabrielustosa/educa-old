from time import sleep

import pytest
from parameterized import parameterized

from educa.tests.base import TestCourseLessonBase


@pytest.mark.slow
@pytest.mark.django_db
class TestQuestionFilter(TestCourseLessonBase):

    @parameterized.expand([
        ('filter', 'filter-i-did', 'Perguntas que eu fiz'),
        ('filter', 'filter-most-answers', 'Perguntas com mais respostas'),
        ('filter', 'filter-most-recent', 'Perguntas mais recentes do curso'),
        ('filter', 'filter-without-answer', 'Perguntas sem respostas'),
        ('filter', 'filter-most-voted', 'Perguntas mais votadas'),
        ('filter-by', 'filter-all', 'Todas as perguntas deste curso'),
        ('filter-by', 'filter-lesson', 'Todas as perguntas da aula'),
    ])
    def test_user_can_filter_question(self, filter_id, element_id, content):
        course = self.load_course()
        self.access_course_view(course)

        self.login()
        self.create_question(course, quantity=6)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable(filter_id)

        self.wait_element_to_be_clickable(element_id)

        sleep(1)

        self.assertIn(
            content,
            self.wait_element_exists('content').text
        )

    @parameterized.expand([
        ('filter', 'filter-i-did', '(1)'),
        ('filter', 'filter-most-answers', '(2)'),
        ('filter', 'filter-most-recent', '(3)'),
        ('filter', 'filter-without-answer', '(4)'),
        ('filter', 'filter-most-voted', '(5)'),
        ('filter-by', 'filter-all', '(6)'),
        ('filter-by', 'filter-lesson', '(7)'),
    ])
    def test_filter_are_showing_correct_length(self, filter_id, element_id, length):
        course = self.load_course()
        self.access_course_view(course)

        self.login()

        quantity = int(length.replace(')', '').replace('(', ''))

        if quantity != 7:
            self.create_question(course, quantity=quantity)
        else:
            self.create_question_for(course.get_first_lesson(), quantity=quantity)

        self.wait_element_to_be_clickable('questions-answers')

        self.wait_element_to_be_clickable(filter_id)

        self.wait_element_to_be_clickable(element_id)

        sleep(1)

        self.assertIn(
            length,
            self.wait_element_exists('content').text
        )
