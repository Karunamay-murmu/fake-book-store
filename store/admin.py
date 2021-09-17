from django.contrib import admin

from store.models import (
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline
    ]
    prepopulated_fields = {
        'slug': ('title',)
    }