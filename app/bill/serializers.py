from rest_framework import serializers

from items.serializers import ItemsListSerializer
from members.serializers import UserSerializer
from .models import Basket, Bill


class BasketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    item = ItemsListSerializer()
    cart_item_pk = serializers.CharField(source='pk', required=False)

    class Meta:
        model = Basket
        fields = ('cart_item_pk', 'user', 'item', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    user_pk = serializers.CharField(source='user.pk')
    cart_items = BasketSerializer(source='basket_set', many=True)
    order_pk = serializers.CharField(source='pk')

    class Meta:
        model = Bill
        fields = (
            'order_pk',
            'user_pk',
            'order_date_time',
            'delivery_date',
            'total_price',
            'cart_items',
        )
        read_only_fields = ('cart_items', 'order_pk')








