from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item, Category
from .serializer import CategorySerializer, ItemsListSerializer, ItemDetailSerializer


# 메인 화면에 카테고리들의 pk를 보내준다
class CategoryItemList(APIView):
    def get(self, request, format=None):
        if not request.query_params:
            # query_params가 비어있으면 Category List 보여주기
            categories = Category.objects.all()
            return Response(CategorySerializer(categories, many=True).data)

        # query_params에서 pk 값을 가져옴
        categories_pk = request.query_params.get('pk')

        # pk로 보내지 않은 경우
        if not categories_pk:
            data = {
                'error': 'parameter를 pk로 보내주세요',
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=categories_pk)
        except Category.DoesNotExist:
            data = {
                'error': '존재하지 않는 category입니다',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        items = Item.objects.filter(categories=category)
        return Response(ItemsListSerializer(items, many=True).data)


class ItemDetail(APIView):
    def get(self, request, format=None):
        item_pk = request.query_params.get('pk')

        # pk로 보내지 않은 경우
        if not item_pk:
            data = {
                'error': 'parameter를 pk로 보내주세요, 또는 parameter를 보내지 않았습니',
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(pk=item_pk)
        except Item.DoesNotExist:
            data = {
                'error': '존재하지 않는 item 입니다',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        return Response(ItemDetailSerializer(item).data)
