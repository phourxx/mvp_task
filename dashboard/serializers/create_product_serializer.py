from rest_framework import serializers

from dashboard.models import Product


class CreateProductSerializer(serializers.ModelSerializer):
    cost = serializers.DecimalField(min_value=5, max_digits=20,
                                    decimal_places=2)
    amountAvailable = serializers.IntegerField(min_value=1)

    class Meta:
        model = Product
        fields = ('productName', 'cost', 'amountAvailable')

    def save(self, **kwargs):
        kwargs['seller'] = self.context['request'].user
        return super(CreateProductSerializer, self).save(**kwargs)
