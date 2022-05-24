from unittest import TestCase

import pytest

from tests.factories.module import ModuleFactory


@pytest.mark.fast
@pytest.mark.django_db
class TestModuleModel(TestCase):

    def test_module_order(self):
        module = ModuleFactory()

        self.assertEqual(module.order, 1)

        module_2 = ModuleFactory(course=module.course)

        self.assertEqual(module_2.order, 2)
