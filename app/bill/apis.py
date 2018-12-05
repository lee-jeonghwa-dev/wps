from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, generics

from items.models import Item
from items.serializers import ItemsListSerializer
from members.permission import IsUser
from .models import Basket, Bill
from .serializers import BasketSerializer, OrderSerializer
from members.serializers import UserSerializer

User = get_user_model()


class ListCreateBasketItemView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = request.user
        baskets = Basket.objects.filter(user=user, order_yn=False)
        serializer = BasketSerializer(baskets, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        try:
            item = Item.objects.get(pk=request.data.get('item_pk'))
        except Item.DoesNotExist:
            data = {'error': '존재하지 않는 item입니다'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if Basket.objects.filter(user=user, item=item, order_yn=False).exists():
            data = {
                'error': '이미 장바구니에 있는 item입니다. patch를 이용해주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        Basket.objects.create(user=user, item=item, amount=request.data.get('amount'))
        baskets = Basket.objects.filter(user=user, order_yn=False)
        serializer = BasketSerializer(baskets, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        user = request.user
        try:
            item = Item.objects.get(pk=request.POST['item_pk'])
        except Item.DoesNotExist:
            data = {'error': '존재하지 않는 item입니다'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        add_amount = request.POST.get('add_amount')
        amount = request.POST.get('amount')

        if add_amount:
            add_amount = int(add_amount)
        if amount:
            amount = int(amount)

        if not Basket.objects.filter(user=user, item=item, order_yn=False).exists():
            data = {
                'error': '아직 장바구니에 없는 item입니다. post를 이용해주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        basket = Basket.objects.get(user=user, item=item, order_yn=False)

        # 예외사항 check
        if add_amount and amount:
            data = {'error': 'add_amount, amount 모두 있습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if not add_amount and not amount:
            data = {'error': 'add_amount, amount 모두 없습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if basket.amount == amount or add_amount == 0:
            data = {'error': 'amount에 변화가 없습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if add_amount:
            if basket.amount + add_amount <= 0:
                data = {'error': 'amount가 0 또는 음수입니다'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            basket.amount += add_amount

        if amount:
            if amount <= 0:
                data = {'error': 'amount가 0 또는 음수입니다'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            basket.amount = amount

        basket.save()
        return self.get(request)

    def delete(self, request):
        user = request.user
        try:
            item = Item.objects.get(pk=request.POST['item_pk'])
        except Item.DoesNotExist:
            data = {'error': '존재하지 않는 item입니다'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        try:
            basket = Basket.objects.get(user=user, item=item, order_yn=False)
        except Basket.DoesNotExist:
            data = {'error': '장바구니에 존재하지 않는 항목입니다'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        basket.delete()

        return self.get(request)


class OrderView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        # IsUser,
    )

    def get(self, request):
        user = request.user
        bills = Bill.objects.filter(user=user).order_by('-order_date_time')
        serializer = OrderSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        a = request.data
        pass
        return Response({'test': 'test'})
