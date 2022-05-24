from random import choice

import pytest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse, resolve
from selenium.webdriver import Keys

from selenium.webdriver.common.by import By

from educa.apps.lesson.models import Lesson
from educa.apps.module.models import Module
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


class FunctionalTestBase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_input_name(self, web_element, name):
        return web_element.find_element(
            By.XPATH, f'//input[@name="{name}"]'
        )

    def get_element_by_id(self, element_id):
        return self.browser.find_element(
            By.ID,
            element_id
        )

    def login(self, username='admin', password='admin', is_superuser=False, user=None):
        form = self.get_element_by_id('login')

        if not user:
            user = UserFactory(username=username)
            user.set_password(password)
            if is_superuser:
                user.is_superuser = True
                user.is_staff = True
            user.save()
        else:
            user.set_password(password)
            user.save()

        username_field = self.get_by_input_name(form, 'username')
        username_field.send_keys(username)

        password_field = self.get_by_input_name(form, 'password')
        password_field.send_keys(password)

        submit = self.get_element_by_id('submit')
        submit.send_keys(Keys.ENTER)

        return user


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


class CourseLessonMixin(ContentMixin):
    def setUp(self):
        self.course = CourseFactory()
        for i in range(5):
            module = ModuleFactory(course=self.course, title=f'title-{i}')
            for n in range(5):
                lesson = LessonFactory(module=module, title=f'title-{n}')
                for j in range(5):
                    content_type_list = ['text', 'image', 'file', 'link']
                    self.create_content(content_type=choice(content_type_list), lesson=lesson, title=f'title-{j}')
        return super().setUp()

    @staticmethod
    def get_lesson_by_id(lesson_id):
        return Lesson.objects.get(id=lesson_id)

    @staticmethod
    def get_module_by_id(module_id):
        return Module.objects.get(id=module_id)
