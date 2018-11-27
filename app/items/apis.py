from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import CategorySerializer # ItemSerializer,
from .models import Item, Category


# class ItemList(APIView):
#     def get(self, request, format=None):
#         items = Item.objects.all()
#         return Response(ItemSerializer(items, many=True).data)


# 메인 화면에 카테고리들의 pk를 보내준다
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)
