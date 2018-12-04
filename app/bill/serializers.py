from rest_framework import serializers

from items.serializers import ItemsListSerializer
from members.serializers import UserSerializer
from .models import Basket


class BasketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    item = ItemsListSerializer()
    cart_item_pk = serializers.CharField(source='pk')

    class Meta:
        model = Basket
        fields = ('cart_item_pk', 'user', 'item', 'amount')

