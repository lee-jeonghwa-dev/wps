from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'pk',
            'item_name',
            'company',
            'origin_price',
            'sale_price',
            'discount_rate',
            'categories',
        )
