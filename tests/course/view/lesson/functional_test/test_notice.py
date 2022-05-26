import pytest

from tests.base import TestCourseLessonBase
from tests.factories.notice import NoticeFactory


@pytest.mark.slow
@pytest.mark.django_db
class TestNotice(TestCourseLessonBase):

    def test_user_can_create_notice(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login(is_superuser=True)

        self.wait_element_to_be_clickable('notice')

        self.wait_element_to_be_clickable('create-notice')

        body = self.wait_element_exists('notice-create')

        title = 'This is a test title.'
        title_input = self.get_by_input_name(body, 'title')
        title_input.send_keys(title)

        content = 'This is a test content.'
        content_input = self.get_by_textarea_name(body, 'content')
        content_input.send_keys(content)

        self.wait_element_to_be_clickable('send')

        self.assertIn(
            'This is a test title.',
            self.wait_element_exists('content').text
        )
        self.assertIn(
            'This is a test content.',
            self.wait_element_exists('content').text
        )

    def test_user_can_update_notice(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login(is_superuser=True)

        NoticeFactory(course=course)

        self.wait_element_to_be_clickable('notice')

        self.wait_element_to_be_clickable('options')

        self.wait_element_to_be_clickable('edit')

        body = self.wait_element_exists('notice-update')

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

    def test_user_can_delete_notice(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login(is_superuser=True)

        notice = NoticeFactory(course=course)

        self.wait_element_to_be_clickable('notice')

        self.wait_element_to_be_clickable('options')

        self.wait_element_to_be_clickable('delete')

        self.wait_element_to_be_clickable('confirm')

        self.assertNotIn(
            notice.title,
            self.wait_element_exists('content').text
        )

        self.assertNotIn(
            notice.content,
            self.wait_element_exists('content').text
        )

    def test_error_message_notice_create(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login(is_superuser=True)

        self.wait_element_to_be_clickable('notice')

        self.wait_element_to_be_clickable('create-notice')

        body = self.wait_element_exists('notice-create')

        title = ''
        title_input = self.get_by_input_name(body, 'title')
        title_input.send_keys(title)

        content = ''
        content_input = self.get_by_textarea_name(body, 'content')
        content_input.send_keys(content)

        self.wait_element_to_be_clickable('send')

        self.assertIn(
            'O título deve conter mais que 5 carácteres.',
            self.wait_element_exists('content').text
        )
        self.assertIn(
            'Os detalhes do seu aviso não podem estar vazios.',
            self.wait_element_exists('content').text
        )

    def test_error_message_notice_update(self):
        course = self.load_course()
        self.access_course_view(course)

        self.login(is_superuser=True)

        NoticeFactory(course=course)

        self.wait_element_to_be_clickable('notice')

        self.wait_element_to_be_clickable('options')

        self.wait_element_to_be_clickable('edit')

        body = self.wait_element_exists('notice-update')

        title = ''
        title_input = self.get_by_input_name(body, 'title')
        title_input.clear()
        title_input.send_keys(title)

        content = ''
        content_input = self.get_by_textarea_name(body, 'content')
        content_input.clear()
        content_input.send_keys(content)

        self.wait_element_to_be_clickable('save')

        self.assertIn(
            'O título deve conter mais que 5 carácteres.',
            self.wait_element_exists('content').text
        )
        self.assertIn(
            'Os detalhes do seu aviso não podem estar vazios.',
            self.wait_element_exists('content').text
        )

