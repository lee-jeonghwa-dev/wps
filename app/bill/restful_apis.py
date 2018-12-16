import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status

from items.models import Item
from members.permission import IsOwner
from .models import Basket, Bill
from .restful_serializers import BasketCreateSerializer, BasketListSerializer

User = get_user_model()


# 장바구니 조회/반찬 추가
class BasketListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def list(self, request, format=None):
        queryset = Basket.objects.filter(order_yn=False, user=request.user)
        serializer = BasketListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, format=None):
        serializer = BasketCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(self.list(request).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasketUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsOwner,
        permissions.IsAuthenticated,
    )

    def retrieve(self, request, pk, format=None):
        cart_item = get_object_or_404(Basket, user=request.user, pk=pk, order_yn=False)
        serializer = BasketListSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, format=None):
        cart_item = get_object_or_404(Basket, user=request.user, order_yn=False, pk=pk)

        if request.data.get('add_amount'):
            amount = cart_item.amount + request.data.get('add_amount')
        else:
            amount = request.data.get('amount')

        if amount < 0 or not amount:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_item.amount = amount
        cart_item.save()
        cart = Basket.objects.filter(user=request.user, order_yn=False)
        return_serializer = BasketListSerializer(cart, many=True)
        return Response(return_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk, format=None):
        cart_item = get_object_or_404(Basket, user=request.user, pk=pk, order_yn=False)
        cart_item.delete()

        cart = Basket.objects.filter(user=request.user, order_yn=False)
        return_serializer = BasketListSerializer(cart, many=True)
        return Response(return_serializer.data, status=status.HTTP_200_OK)


# 주문
class OrderView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = request.user
        bills = Bill.objects.filter(user=user).order_by('-order_date_time')
        serializer = OrderSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    @transaction.atomic
    def post(self, request):
        sid = transaction.savepoint()
        user = request.user
        address = request.data.get('address')
        delivery_date = request.data.get('delivery_date')
        order_item_list = request.data.get('order_item_list')
        total_price = request.data.get('total_price')
        check_price = 0

        if not (user and address and delivery_date and order_item_list and total_price):
            data = {
                'error': '입력한 조건으로 주문이 불가능 합니다'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            bill = Bill.objects.create(
                user=user,
                address=address,
                delivery_date=delivery_date,
                total_price=total_price
            )
        except Bill.DoesNotExist:
            data = {
                'error': '입력한 조건으로 주문이 불가능 합니다'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        for order_item in order_item_list:
            cart_item_pk = order_item['cart_item_pk']
            try:
                order_item = Basket.objects.get(pk=cart_item_pk, user=user, order_yn=False)
            except Basket.DoesNotExist:
                data = {
                    'error': '장바구니에 존재하지 않는 item을 주문하려고 합니다'
                }
                transaction.savepoint_rollback(sid)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            order_item.order = bill
            order_item.order_yn = True
            order_item.save()
            check_price += order_item.item.sale_price * order_item.amount

        if check_price < 40000:
            check_price += 2500
        if check_price != total_price:
            data = {
                'error': '결제시도 금액이 실제 가격과 다릅니다'
            }
            transaction.savepoint_rollback(sid)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d')
        order_date_time = bill.order_date_time + datetime.timedelta(hours=9)
        order_date_time = order_date_time.replace(tzinfo=None)

        if delivery_date < order_date_time:
            data = {
                'error': '배달 요청일이 주문일보다 빠릅니다'
            }
            transaction.savepoint_rollback(sid)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        transaction.savepoint_commit(sid)
        return Response(OrderSerializer(bill).data, status=status.HTTP_200_OK)
