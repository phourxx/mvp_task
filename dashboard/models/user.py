from decimal import Decimal
from typing import List

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from safedelete.managers import SafeDeleteManager as BaseSafeDeleteManager

from mvp_task.constants import SELLER_ROLE, BUYER_ROLE, AMOUNT_CHOICES, ROLES
from mvp_task.utils import log_exception


class SafeDeleteManager(BaseSafeDeleteManager, UserManager):
    pass


class User(AbstractUser):
    """
        Overrides django's default auth model
    """
    first_name = None
    last_name = None
    REQUIRED_FIELDS = ["password", "role"]
    USERNAME_FIELD = 'username'
    deposit = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    role = models.CharField(choices=ROLES.items(), null=False, blank=False,
                            max_length=10)
    updatedAt = models.DateTimeField(auto_now=True)

    @property
    def is_seller(self):
        return self.role == SELLER_ROLE

    @property
    def is_buyer(self):
        return self.role == BUYER_ROLE

    def can_afford_amount(self, amount: Decimal) -> bool:
        return self.deposit >= amount

    def deduct_amount(self, amount: Decimal):
        self.deposit -= amount
        self.save()

    @property
    def deposit_breakdown(self) -> List:
        breakdown = []
        try:
            balance = self.deposit
            if self.deposit == 0:
                return breakdown

            denominations = sorted(AMOUNT_CHOICES, reverse=True)
            for denomination in denominations:
                if balance >= denomination:
                    multiple = balance // denomination
                    for _ in range(int(multiple)):
                        breakdown.append(denomination)
                    balance -= denomination * multiple
        except Exception as ex:
            log_exception(type(self).__name__, ex)

        return breakdown
