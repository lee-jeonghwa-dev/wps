import datetime

from django.db import transaction
from rest_framework import serializers

from items.models import Item
from items.new_serializers import ItemsSimpleSerializer
from members.new_serializers import UserSerializer
from .models import Basket, Bill


class BasketListSerializer(serializers.ModelSerializer):
    item = ItemsSimpleSerializer()

    class Meta:
        model = Basket
        fields = ('pk', 'user', 'item', 'amount')


class BasketCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Basket
        fields = ('pk', 'user', 'item', 'amount')
        read_only_fields = ('user',)

    def validate(self, data):
        data
        if Basket.objects.filter(item=data['item'], user=data['user'], order_yn=False).exists():
            raise serializers.ValidationError('이미 장바구니에 존재하는 반찬입니다')
        return data

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('주문량이 0보다 작습니다')
        return value


class OrderListSerializer(serializers.ModelSerializer):
    cart_items = BasketListSerializer(source='basket_set', many=True)

    class Meta:
        model = Bill
        fields = (
            'pk',
            'user',
            'order_date_time',
            'delivery_date',
            'total_price',
            'address',
            'cart_items',
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Bill
        fields = (
            'pk',
            'user',
            'order_date_time',
            'delivery_date',
            'total_price',
            'address',
            'basket_set',
        )
        read_only_fields = (
            'user',
        )

    def validate(self, data):
        check_total_price = 0
        cart_items = data.get('basket_set')

        for cart_item in cart_items:
            if cart_item.user == data.get('user') and cart_item.order_yn == False:
                check_total_price += cart_item.item.sale_price * cart_item.amount
            else:
                raise serializers.ValidationError('현재 사용자에게 없는 장바구니 목록입니다')

        if check_total_price < 40000:
            check_total_price += 2500

        if check_total_price != data.get('total_price'):
            raise serializers.ValidationError('최종 금액이 올바르지 않습니다')

        return data

    def validate_delivery_date(self, value):
        #  배송일이 주문일보다 빠르면
        if value < datetime.date.today():
            raise serializers.ValidationError('배송일이 주문일 보다 빠릅니다')
        return value

    def create(self, validated_data):
        cart_items = validated_data.pop('basket_set')
        bill = Bill.objects.create(**validated_data)
        for cart_item in cart_items:
            cart_item.order_yn = True
            cart_item.order = bill
            cart_item.save()

        return bill














