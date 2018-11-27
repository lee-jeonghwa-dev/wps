from rest_framework import serializers

from .models import Item, Category, ItemImage


# category 종류를 보여줌
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'pk',
            'main_category',
            'sub_category',
        )


# ListThumbnail (ItemImage 에서 type='L' 만 필요할 때 사용하는 serializer
class ListThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('photo',)


# 반찬 List를 보여주는 page에 필요한 serializer
class ItemsListSerializer(serializers.Serializer):
    item_name = serializers.CharField(max_length=150)
    company = serializers.CharField(max_length=50)
    origin_price = serializers.IntegerField()
    sale_price = serializers.IntegerField()
    discount_rate = serializers.FloatField(default=0.0)
    photo = serializers.ImageField()

    def to_representation(self, instance):
        data = {
            'item_name': instance.item.item_name,
            'company': instance.item.company,
            'origin_price': instance.item.origin_price,
            'sale_price': instance.item.sale_price,
            'discount_rate': instance.item.discount_rate,
            'photo': ListThumbnailSerializer(instance).data
        }
        return data



