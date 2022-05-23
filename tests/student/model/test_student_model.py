from unittest import TestCase

import pytest

from tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestStudentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = UserFactory._meta.model

    def test_user_crud(self):
        user = UserFactory()

        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.password, 'admin123')

        user.username = 'Admin'
        user.password = 'Admin123'
        user.save()

        self.assertEqual(user.username, 'Admin')
        self.assertEqual(user.password, 'Admin123')
