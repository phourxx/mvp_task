from rest_framework import serializers

from dashboard.models import Product


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'productName', 'slug', 'cost', 'amountAvailable')


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(source='seller.username')

    class Meta:
        model = Product
        fields = '__all__'
