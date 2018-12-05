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

    def create(self, validated_data):
        user = validated_data.get('user')
        item = validated_data.get('item')
        amount = validated_data('amount')
        if Basket.objects.filter(user=user, item=item, order_yn=False):
            raise serializers.ValidationError('이미 장바구니에 있는 item입니다. patch를 이용해주세요')

        basket = Basket.objects.create(user=user, item=item, amount=amount)
        return basket


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
            'cart_items',

        )






