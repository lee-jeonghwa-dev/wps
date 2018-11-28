from rest_framework import serializers

from .models import Item, Category, ItemImage, Description


# category 종류를 보여줌
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'pk',
            'main_category',
            'sub_category',
            'photo',
        )


# 반찬 List를 보여주는 page에 필요한 serializer
class ItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'pk',
            'company',
            'item_name',
            'origin_price',
            'sale_price',
            'discount_rate',
            'list_thumbnail',
        )


class ItemDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = '__all__'


class ItemDetailSerializer(serializers.ModelSerializer):
    description = ItemDescriptionSerializer()
    itemimage_set = ItemImageSerializer(many=True)

    class Meta:
        model = Item
        fields = (
            'pk',
            'company',
            'item_name',
            'origin_price',
            'sale_price',
            'discount_rate',
            'description',
            'itemimage_set'
        )





