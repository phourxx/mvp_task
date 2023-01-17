from django.db import models

from dashboard.models import BaseModelAbstract, User, Product


class Purchase(BaseModelAbstract):
    buyer = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)
    product = models.ForeignKey(Product, models.DO_NOTHING, null=False,
                                blank=False)
    quantity = models.IntegerField(default=1)
    unit_cost = models.DecimalField(decimal_places=2, max_digits=20,
                                    null=False, blank=False)
    total_cost = models.DecimalField(decimal_places=2, max_digits=20,
                                     null=False, blank=False)
