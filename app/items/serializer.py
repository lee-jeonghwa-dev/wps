from rest_framework import serializers

from .models import Item, Category


# category 종류를 보여줌
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'pk',
            'main_category',
            'sub_category',
        )


# 반찬 List를 보여주는 page에 필요한 serializer
# class ItemsListSerializer(serializers.ModelSerializer):
#     list_thumbnail =
#     class Meta:
#         model = Item
#         fields = (
#             'pk',
#             'item_name',
#             'company',
#             'origin_price',
#             'sale_price',
#             'discount_rate',
#             'categories',
#         )


