from rest_framework import serializers
from dashboard.models import Product


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('productName', 'cost')
