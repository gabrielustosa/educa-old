import pytest
import time

from random import choice

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse, resolve

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.factories.course import CourseFactory
from tests.factories.lesson import LessonFactory
from tests.factories.module import ModuleFactory
from tests.factories.user import UserFactory
from utils.browser import make_chrome_browser
from educa.apps.content.models import Text, Content, File, Image, Link


@pytest.mark.django_db
class ContentMixin:
    def create_content(
            self,
            content_type,
            owner=None,
            lesson=None,
            title='teste',
            content='teste',
            file='teste',
            image='teste',
            url='teste',
    ):
        if not owner:
            owner = UserFactory(username='teste')
        if not lesson:
            lesson = LessonFactory(course__owner=owner)
        obj = None
        match content_type:
            case 'text':
                obj = Text.objects.create(title=title, content=content, owner=owner)
                Content.objects.create(item=obj, lesson=lesson)
            case 'file':
                obj = File.objects.create(title=title, file=file, owner=owner)
                Content.objects.create(item=obj, lesson=lesson)
            case 'image':
                obj = Image.objects.create(title=title, image=image, owner=owner)
                Content.objects.create(item=obj, lesson=lesson)
            case 'link':
                obj = Link.objects.create(title=title, url=url, owner=owner)
                Content.objects.create(item=obj, lesson=lesson)
        return obj

    def create_content_in_batch(
            self,
            content_type,
            batch=1,
            owner=None,
            lesson=None,
            title='teste',
            content='teste',
            file='teste',
            image='teste',
            url='teste',
    ):
        for i in range(batch):
            self.create_content(
                content_type=content_type, owner=owner,
                lesson=lesson, title=title,
                content=content, file=file,
                image=image, url=url
            )


class TestFunctionalBase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        self.wait = WebDriverWait(self.browser, 20)
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_input_name(self, web_element, name):
        return web_element.find_element(
            By.XPATH, f'//input[@name="{name}"]'
        )

    def get_by_textarea_name(self, web_element, name):
        return web_element.find_element(
            By.XPATH, f'//textarea[@name="{name}"]'
        )

    def login(self, username='admin', password='admin', is_superuser=False):
        form = self.browser.find_element(By.ID, 'login')

        user = UserFactory(username=username)
        user.set_password(password)
        if is_superuser:
            user.is_superuser = True
            user.is_staff = True
        user.save()

        username_field = self.get_by_input_name(form, 'username')
        username_field.send_keys(username)

        password_field = self.get_by_input_name(form, 'password')
        password_field.send_keys(password)

        submit = self.browser.find_element(By.ID, 'submit')
        submit.send_keys(Keys.ENTER)

        return user

    def wait_element_to_be_clickable(self, element_id, max_wait=20):
        start_time = time.time()
        while True:
            try:
                self.browser.find_element(By.ID, element_id).click()
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > max_wait:
                    raise e
                time.sleep(0.5)

    def wait_element_exists(self, element_id):
        return self.wait.until(expected_conditions.visibility_of_element_located((By.ID, element_id)))


class TestCustomBase(TestCase):
    def response_post(self, url, data=None, **kwargs):
        if data is None:
            data = {}
        return self.client.post(reverse(url, **kwargs), data)

    def response_get(self, url, **kwargs):
        return self.client.get(reverse(url, **kwargs))

    def get_view(self, url, **kwargs):
        return resolve(reverse(url, **kwargs))

    def login(self, username='admin', password='admin', is_superuser=False):
        user = UserFactory(username=username)
        user.set_password(password)
        if is_superuser:
            user.is_superuser = True
            user.is_staff = True
        user.save()

        self.client.login(username=username, password=password)

        return user


class TestCourseLessonMixin(ContentMixin):
    def load_course(self):
        course = CourseFactory()
        for i in range(5):
            module = ModuleFactory(course=course, title=f'title-{i}')
            for n in range(5):
                lesson = LessonFactory(course=course, module=module, title=f'title-{n}')
                for j in range(5):
                    content_type_list = ['text', 'image', 'file', 'link']
                    self.create_content(content_type=choice(content_type_list), lesson=lesson, title=f'title-{j}')
        return course


class TestCourseLessonBase(TestFunctionalBase, TestCourseLessonMixin):
    def access_course_view(self, course):
        self.browser.get(self.live_server_url + reverse('student:view',
                                                        kwargs={'course_slug': course.slug,
                                                                'lesson_id': course.get_first_lesson_id()}))

    def ask_question(self):
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
