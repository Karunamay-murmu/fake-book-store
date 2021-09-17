from django.http import response
from django.test import TestCase

from category.models import Category


class TestCategoriesModel(TestCase):

    def setUp(self) -> None:
        self.data1 = Category.objects.create(name="test", slug="test")
        return super().setUp()

    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_return_name(self):
        '''
        Test category model name
        '''
        data = self.data1
        self.assertEqual(str(data), 'test')