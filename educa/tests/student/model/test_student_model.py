from unittest import TestCase

import pytest

from educa.tests.factories.user import UserFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestStudentModel(TestCase):
    def test_user_crud(self):
        user = UserFactory(email='tester@gmail.com', name='Tester da Silva')

        self.assertEqual(user.email, 'tester@gmail.com')
        self.assertEqual(user.name, 'Tester da Silva')

        user.email = 'tester2@gmail.com'
        user.name = 'Tester Lustosa'
        user.save()

        self.assertEqual(user.email, 'tester2@gmail.com')
        self.assertEqual(user.name, 'Tester Lustosa')
