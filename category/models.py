from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey



class Category(MPTTModel):

    # Category TABLE implemeted with MPTT 
    name = models.CharField(verbose_name=_("category name"), help_text=_("Required and Unique"), max_length=255, unique=True)
    slug = models.SlugField(verbose_name=_("category safe url"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Caetgory")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("category:category_product_list", args=[self.slug])

    def __str__(self):
        return self.name


