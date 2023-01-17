from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from .base import BaseModelAbstract


class Product(BaseModelAbstract):
    productName = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True, max_length=255)
    amountAvailable = models.IntegerField(default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=20, null=False,
                               blank=False)
    seller = models.ForeignKey(get_user_model(),
                               on_delete=models.DO_NOTHING, null=False,
                               blank=False, related_name='products')

    def is_available_for_qty(self, qty) -> bool:
        return self.amountAvailable > 0 and self.amountAvailable > qty

    def get_total_for_qty(self, qty: int) -> Decimal:
        return self.cost * Decimal(qty)

    def save(self, keep_deleted=False, **kwargs):
        self.slug = slugify(self.productName)
        super(Product, self).save(**kwargs)
