from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from category.models import Category
    


class ProductType(models.Model):

    # ProductType TABLE will provide a list of the different types of product that are for sale.
    name = models.CharField(verbose_name=_("product type"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name



class ProductSpecification(models.Model):
    
    # ProductSpicification TABLE store product specification,
    # or features for a perticular product type.
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, related_name="prod_spec")
    name = models.CharField(verbose_name=_("name"), help_text=_("Required"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name



class Product(models.Model):

    # Product TABLE containing all the product items.
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    description = models.TextField(verbose_name=_("description"), help_text=_("Not required"), max_length=500, blank=True)
    slug = models.SlugField(max_length=255)
    avg_rating = models.CharField(verbose_name=_("avarage rating"), blank=True, null=True, max_length=5)
    rating_count = models.CharField(verbose_name=_("total rating count"), blank=True, null=True, max_length=255)
    regular_price = models.DecimalField(
                        verbose_name=_("regular price"), 
                        help_text=_("maximum 999.99"), 
                        max_digits=10, 
                        decimal_places=2,
                        error_messages={
                            "name": {
                                "max_length": _("The price must be between 0 and 999.99"),
                            }
                        },
                        default='109.99'
                    )
    discount_price = models.DecimalField(
                        verbose_name=_("discount price"), 
                        help_text=_("maximum 999.99"), 
                        max_digits=10, 
                        decimal_places=2,
                        error_messages={
                            "name": {
                                "max_length": _("The price must be between 0 and 999.99"),
                            }
                        }
                    )
    wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="wishlist", blank=True)
    is_active = models.BooleanField(verbose_name=_("product available"), help_text=_("Change product availability"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.product_type.name, self.slug])

    def __str__(self):
        return self.slug
        


class ProductSpecificationValue(models.Model):

    # ProductSpecificationValue TABLE holds each products
    # individual specification or features
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='spec')
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT, related_name="spec_name")
    value = models.CharField(verbose_name=_("value"), help_text=_("Product specification value"), max_length=255)

    class Meta:
        verbose_name = _("Product specification value")
        verbose_name_plural = _("Product specification value")

    # def __str__(self):
    #     return self.value



class ProductImage(models.Model):

    # Product image table
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(
                verbose_name=_("image"),
                help_text=_("Upload a product image"),
                upload_to="images/",
                default="images/default.png"
            )
    alt_text = models.CharField(
                    verbose_name=_("alternative text"),
                    help_text=_("Add a alternative text"),
                    max_length=255,
                    null=True,
                    blank=True
                )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

