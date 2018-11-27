from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import CategorySerializer, ItemsListSerializer
from .models import Item, Category, ItemImage


class ItemList(APIView):
    def get(self, request, categories_pk, format=None):
        try:
            category = Category.objects.get(pk=categories_pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # ItemImage에 innerjoin을 이용하여 item을 같이 가져옴
        items = ItemImage.objects.select_related().filter(photo_type='L', item__categories__pk=categories_pk)

        return Response(ItemsListSerializer(items, many=True).data)


# 메인 화면에 카테고리들의 pk를 보내준다
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)
