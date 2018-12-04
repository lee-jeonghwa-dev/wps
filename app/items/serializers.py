from rest_framework import serializers

from .models import Item, Category, ItemImage, Description


# category 종류를 보여줌
class CategorySerializer(serializers.ModelSerializer):
    category_pk = serializers.CharField(source='pk')

    class Meta:
        model = Category
        fields = (
            'category_pk',
            'main_category',
            'sub_category',
            'photo',
        )


# 반찬 List를 보여주는 page에 필요한 serializer
class ItemsListSerializer(serializers.ModelSerializer):
    item_pk = serializers.CharField(source='pk')

    class Meta:
        model = Item
        fields = (
            'item_pk',
            'company',
            'item_name',
            'origin_price',
            'sale_price',
            'discount_rate',
            'list_thumbnail',
        )


# Description의 Serializer
class ItemDescriptionSerializer(serializers.ModelSerializer):
    description_pk = serializers.CharField(source='pk')
    item_pk = serializers.CharField(source='item.pk')

    class Meta:
        model = Description
        fields = (
            'item_pk',
            'description_pk',
            'added_words',
            'point',
            'delivery_type',
            'receive_day',
            'regular_delivery',
            'item_type',
            'factory_address',
            'dom',
            'capacity',
            'ingredient',
            'allergy_material',
            'caution',
        )


# ItemImage의 Serializer
class ItemImageSerializer(serializers.ModelSerializer):
    item_image_pk = serializers.CharField(source='pk')
    item_pk = serializers.CharField(source='item.pk')

    class Meta:
        model = ItemImage
        fields = (
            'item_pk',
            'item_image_pk',
            'photo_type',
            'image_order',
            'photo'
        )


# Item 상세페이지에서 필요한 정보를 제공함
class ItemDetailSerializer(serializers.ModelSerializer):
    description = ItemDescriptionSerializer()
    itemimage_set = ItemImageSerializer(many=True)

    item_pk = serializers.CharField(source='pk')

    class Meta:
        model = Item
        fields = (
            'item_pk',
            'company',
            'item_name',
            'origin_price',
            'sale_price',
            'discount_rate',
            'description',
            'itemimage_set'
        )





