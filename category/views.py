from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView

from category.models import Category
from store.models import Product

class CategoryProductList(ListView):
    model = Category
    template_name = 'category/category_product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category__in=Category.objects.get(slug=slug).get_descendants(include_self=True))

        context['category'] = category
        context['products'] = products

        return context