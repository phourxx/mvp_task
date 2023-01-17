from django.db import models

from dashboard.models import BaseModelAbstract, Product


class Inventory(BaseModelAbstract):
    product = models.ForeignKey(Product, models.DO_NOTHING, null=False,
                                blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    quantity_before = models.IntegerField(default=0)
    quantity_after = models.IntegerField(null=False, blank=False)
