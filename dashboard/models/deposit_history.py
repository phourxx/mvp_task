from django.db import models

from .user import User
from .base import BaseModelAbstract


class DepositHistory(BaseModelAbstract):
    user = models.ForeignKey(User, models.DO_NOTHING,
                             null=False, blank=False)
    amount = models.DecimalField(decimal_places=2, max_digits=20,
                                 null=False, blank=False)
    deposit_before = models.DecimalField(decimal_places=2, max_digits=20,
                                         null=False, blank=False)
    deposit_after = models.DecimalField(decimal_places=2, max_digits=20,
                                        null=False, blank=False)
