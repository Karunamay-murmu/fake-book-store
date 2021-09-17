from django.http import response
from django.test import TestCase, Client, client
from django.urls import reverse

from category.models import Category
from store.models import Product
from store.views import home, product_detail



class TestViewResponses(TestCase):

    def setUp(self) -> None:
        self.c = Client()
        Category.objects.create(name="test", slug="test")
        return super().setUp()

    def test_category_detail_url(self) -> None:
        response = self.c.get(reverse("category:category_product_list", args=['test']))
        self.assertEqual(response.status_code, 200)
