from django.test import TestCase

from store.models import Product
from category.models import Category


class TestProductModel(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(name="test", slug="test")
        self.product = Product.objects.create(
            name="book name",
            author="admin",
            publisher="admin",
            pages=20,
            language="english",
            category_id=1,
            ISBN="123456",
            slug="book-name",
            price=20,
            stock=5,
        )
        return super().setUp()

    def test_product_model_entry(self):
        '''
        Test product insertation in database
        '''
        data = self.product
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'book name')

