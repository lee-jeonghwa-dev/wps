from rest_framework import serializers

from .models import Item, Category, ItemImage, Description, Comment


# category 종류를 보여줌
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'pk',
            'main_category',
            'sub_category',
            'photo'
        )


# 반찬 List를 보여주는 page에 필요한 serializer
class ItemsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'pk',
            'item_name',
            'company',
            'origin_price',
            'sale_price',
            'discount_rate',
            'list_thumbnail',
        )


# Description의 Serializer
class ItemDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = (
            'pk',
            'item',
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

    class Meta:
        model = ItemImage
        fields = (
            'pk',
            'item',
            'photo_type',
            'image_order',
            'photo'
        )


# 댓글
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'item',
            'content',
            'nickname',
        )
        read_only_fields = ('nickname', )


# Item 상세페이지에서 필요한 정보를 제공함
class ItemDetailSerializer(serializers.ModelSerializer):
    description = ItemDescriptionSerializer()
    itemimage_set = ItemImageSerializer(many=True)
    comment_set = CommentSerializer(many=True)

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
            'itemimage_set',
            'comment_set'
        )


