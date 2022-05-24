from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse, resolve

from selenium.webdriver.common.by import By

from tests.factories.user import UserFactory
from utils.browser import make_chrome_browser


class FunctionalTestBase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser('--headless')
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
