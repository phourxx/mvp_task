from rest_framework import serializers

from dashboard.models import Purchase, Product, DepositHistory
from mvp_task import errors


class PurchaseSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(min_value=1)
    product = None

    class Meta:
        model = Purchase
        fields = ('productId', 'quantity')

    def validate(self, attrs):
        try:
            qty = attrs['quantity']
            user = self.context['request'].user
            self.product = Product.objects.get(pk=attrs['productId'])
            if not self.product.is_available_for_qty(qty):
                raise serializers.ValidationError(errors.QTY_EXCEEDED_ERROR)

            total = self.product.get_total_for_qty(qty)
            if not user.can_afford_amount(total):
                raise serializers.ValidationError(
                    errors.INSUFFICIENT_BAL_ERROR
                )
        except Product.DoesNotExist:
            raise serializers.ValidationError(errors.INVALID_PRODUCT_ID_ERROR)
        return attrs

    def _create_deposit_history(self, user, amount):
        DepositHistory.objects.create(
            user=user,
            amount=f"-{amount}",
            deposit_before=user.deposit,
            deposit_after=user.deposit-amount
        )

    def create(self, validated_data):
        data = validated_data
        user = self.context['request'].user
        total = self.product.get_total_for_qty(data['quantity'])
        data['buyer'] = user
        data['product'] = self.product
        data['unit_cost'] = self.product.cost
        data['total_cost'] = total
        del data['productId']

        self._create_deposit_history(user, total)
        user.deduct_amount(total)

        self.product.amountAvailable -= 1
        self.product.save()

        return super(PurchaseSerializer, self).create(data)
