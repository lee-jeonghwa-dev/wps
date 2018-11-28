from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item, Category, ItemImage
from .serializer import CategorySerializer, ItemsListSerializer, ItemDetailSerializer


class ItemList(APIView):
    def get(self, request, categories_pk, format=None):
        try:
            category = Category.objects.get(pk=categories_pk)
        except Category.DoesNotExist:
            data = {
                'error': '존재하지 않는 category입니다',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        items = Item.objects.filter(categories=category)
        return Response(ItemsListSerializer(items, many=True).data)


# 메인 화면에 카테고리들의 pk를 보내준다
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)


class ItemDetail(APIView):
    def get(self, request, item_pk, format=None):
        try:
            item = Item.objects.get(pk=item_pk)
        except Item.DoesNotExist:
            data = {
                'error': '존재하지 않는 item 입니다',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        return Response(ItemDetailSerializer(item).data)
