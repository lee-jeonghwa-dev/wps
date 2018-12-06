from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemsListSerializer

class SearchView(APIView):

    def get(self, request, format=None):
        if not request.query_params:
            data = {
                'error': '검색어를 입력해 주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        search_str = request.query_params.get('search_str')

        if not search_str:
            data = {
                'error': '검색어를 입력해 주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        items = Item.objects.filter(item_name__contains=search_str) | \
                Item.objects.filter(company__contains=search_str) | \
                Item.objects.filter(description__item_type__contains=search_str)

        serializer = ItemsListSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




