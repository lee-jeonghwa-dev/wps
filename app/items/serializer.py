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


# # 반찬 하나에 대한 내용 (list에 들어가는 내용)
# class ItemsSerializer(serializers.ModelSerializer):
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
#

