from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.db.models import Q

from decimal import Decimal

from store.models import Product, ProductSpecificationValue
from category.models import Category


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.prefetch_related(
            'category', 'spec__specification', 'product_type', 'image').filter(is_active=True)
        return context



class Shop(ListView):
    template_name = 'store/shop.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        prefetch_products = Product.objects.all().prefetch_related(
            'category', 'spec', 'spec__specification', 'product_type', 'image',)

        if 'category' in self.request.GET:
            category_slug = self.request.GET['category']
            prefetch_products = prefetch_products.filter(
                category__slug__exact=category_slug)

        if 'author' in self.request.GET:
            author = self.request.GET['author']
            prefetch_products = prefetch_products.filter(
                spec__value__iexact=author)

        if 'p_min' and 'p_max' in self.request.GET:
            price_min = self.request.GET['p_min']
            price_max = self.request.GET['p_max']
            prefetch_products = prefetch_products.filter(
                discount_price__gte=Decimal(price_min), discount_price__lte=Decimal(price_max))

        return prefetch_products

    def get_context_data(self):
        context = super().get_context_data()
        if not self.request.META['QUERY_STRING'] or 'p_min' and 'p_max' in self.request.GET:
            specs = ProductSpecificationValue.objects.all().select_related('specification')
            authors = []
            for spec in specs:
                if spec.specification.name == 'author' and spec.value not in authors:
                    authors.append(spec.value)
            context['authors'] = authors

        return context



class ProductDetail(TemplateView):
    template_name = "store/product/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prefetch_products = Product.objects.prefetch_related(
            'category', 'spec', 'spec__specification', 'product_type', 'image',)
        product = get_object_or_404(prefetch_products, slug=kwargs['slug'])

        for spec in product.spec.all():
            if spec.specification.name == 'author':
                author_name = spec.value
                author_products = prefetch_products.filter(spec__value__iexact=author_name).prefetch_related(
            'category', 'spec', 'spec__specification', 'product_type', 'image',)
    
        category_products = prefetch_products.filter(category__name=product.category.name).prefetch_related(
            'category', 'spec', 'spec__specification', 'product_type', 'image',)

        context['author_products'] = author_products
        context['author_name'] = author_name
        context['product'] = product
        context['category_products'] = category_products

        return context



class Search(TemplateView):
    template_name = 'store/search/search.html'

    def get_context_data(self):
        context = super().get_context_data()
        if 'query' in self.request.GET:
            query = self.request.GET['query']
            products = Product.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
            context['products'] = products
        return context

    
