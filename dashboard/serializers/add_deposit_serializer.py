from decimal import Decimal

from rest_framework import serializers

from dashboard.models import DepositHistory
from mvp_task.constants import AMOUNT_CHOICES


class AddDepositSerializer(serializers.ModelSerializer):
    amount = serializers.ChoiceField(
        choices=AMOUNT_CHOICES
    )
    balance = serializers.CharField(source='deposit_after', read_only=True)

    class Meta:
        model = DepositHistory
        fields = ('amount', 'balance')

    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['user'] = user
        kwargs['deposit_before'] = user.deposit
        user.deposit += Decimal(self.validated_data['amount'])
        kwargs['deposit_after'] = user.deposit
        instance = super(AddDepositSerializer, self).save(**kwargs)
        user.save()
        return instance
