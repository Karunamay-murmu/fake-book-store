from django.urls import path

from category.views import CategoryProductList

app_name = 'category'

urlpatterns = [
    path('<slug:slug>', CategoryProductList.as_view(), name='category_product_list')
]
