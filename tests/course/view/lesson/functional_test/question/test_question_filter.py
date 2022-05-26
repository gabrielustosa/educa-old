import pytest
from parameterized import parameterized

from tests.base import TestCourseLessonBase


@pytest.mark.slow
@pytest.mark.django_db
class TestQuestionFilter(TestCourseLessonBase):

    @parameterized.expand([
        ('filter', 'filter-i-did', 'Perguntas que eu fiz'),
        ('filter', 'filter-more-answers', 'Perguntas com mais respostas'),
        ('filter', 'filter-more-recent', 'Perguntas mais recentes do curso'),
        ('filter', 'filter-without-answer', 'Perguntas sem respostas'),
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

        self.assertIn(
            content,
            self.wait_element_exists('content').text
        )
