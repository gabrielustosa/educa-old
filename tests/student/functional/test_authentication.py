import pytest
from django.urls import reverse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from tests.base import TestFunctionalBase
from tests.factories.user import UserFactory


@pytest.mark.functional_test
class TestFunctionalRegister(TestFunctionalBase):

    def test_user_can_register(self):
        self.browser.get(self.live_server_url + reverse('register'))

        form = self.browser.find_element(By.ID, 'register')

        username_field = self.get_by_input_name(form, 'username')
        username_field.send_keys('admin')

        email_field = self.get_by_input_name(form, 'email')
        email_field.send_keys('admin@test.com')

        password1_field = self.get_by_input_name(form, 'password1')
        password1_field.send_keys('admin4615#$%')

        password2_field = self.get_by_input_name(form, 'password2')
        password2_field.send_keys('admin4615#$%')

        submit = self.browser.find_element(By.ID, 'submit')
        submit.send_keys(Keys.ENTER)

        self.assertEqual(self.live_server_url + reverse('home'), self.live_server_url + reverse('home'))


class TestFunctionalLogin(TestFunctionalBase):

    def test_user_can_login(self):
        self.browser.get(self.live_server_url + reverse('login'))

        form = self.browser.find_element(By.ID, 'login')

        username = 'admin'
        password = 'admin4615#$%'
        UserFactory(username=username, password=password)

        username_field = self.get_by_input_name(form, 'username')
        username_field.send_keys(username)

        password_field = self.get_by_input_name(form, 'password')
        password_field.send_keys(password)

        submit = self.browser.find_element(By.ID, 'submit')
        submit.send_keys(Keys.ENTER)

        self.assertEqual(self.live_server_url + reverse('home'), self.live_server_url + reverse('home'))
