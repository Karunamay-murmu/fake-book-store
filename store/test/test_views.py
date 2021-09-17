from django.test import TestCase, Client
from django.urls import reverse

from category.models import Category
from store.models import Product
from store.views import home, product_detail


 
class TestViewResponses(TestCase):

    def setUp(self) -> None:
        self.c = Client()
        Category.objects.create(name="test", slug="test")
        Product.objects.create(
            name="book name",
            author="admin",
            publisher="admin",
            pages=20,
            language="english",
            image='image',
            category_id=1,
            ISBN="123456",
            slug="book-name",
            price=20,
            stock=5,
        )
        return super().setUp()

    def test_allowed_host(self) -> None:
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self) -> None:
        response = self.c.get(reverse('store:product_detail', args=['book-name']))
        self.assertEqual(response.status_code, 200)