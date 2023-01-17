from rest_framework import serializers

from dashboard.models import Product, Inventory
from mvp_task import errors


class InventorySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    productId = serializers.IntegerField(min_value=1)
    product = None

    class Meta:
        model = Inventory
        fields = ('productId', 'quantity')

    def validate(self, attrs):
        try:
            user = self.context['request'].user
            self.product = user.products.get(pk=attrs['productId'])
        except Product.DoesNotExist:
            raise serializers.ValidationError(errors.INVALID_PRODUCT_ID_ERROR)
        return attrs

    def _update_product_object(self, qty):
        self.product.amountAvailable += qty
        self.product.save()

    def create(self, validated_data):
        data = validated_data
        current = self.product.amountAvailable
        data['product'] = self.product
        data['quantity_before'] = current
        data['quantity_after'] = current + data['quantity']
        del data['productId']

        self._update_product_object(data['quantity'])

        return super(InventorySerializer, self).create(data)
