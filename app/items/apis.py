from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import ItemSerializer
from .models import Item


class ItemList(APIView):
    def get(self, request, format=None):
        items = Item.objects.all()
        return Response(ItemSerializer(items, many=True).data)
