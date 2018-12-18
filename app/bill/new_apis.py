from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, mixins

from members.permission import IsOwner
from .models import Basket, Bill
from .new_serializers import BasketCreateSerializer, BasketListSerializer, OrderListSerializer, OrderCreateSerializer

User = get_user_model()


# 장바구니 조회/item(반찬) 추가
class BasketListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        return Basket.objects.filter(order_yn=False, user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BasketListSerializer
        elif self.request.method == 'POST':
            return BasketCreateSerializer

    def create(self, request, format=None):
        serializer = BasketCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            cart_items = Basket.objects.filter(user=request.user, order_yn=False)
            return_serializer = BasketListSerializer(cart_items, many=True)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 장바구니 수량변경, 아이템(반찬)삭제, 장바구니 한 항목 가져오기
class BasketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsOwner,
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        return Basket.objects.filter(order_yn=False, user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BasketListSerializer
        elif self.request.method == 'PATCH':
            return BasketCreateSerializer
        elif self.request.method == 'DELETE':
            return BasketCreateSerializer

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


# 주문 전체 조회, 주문 생성
class OrderListCreateView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = request.user
        bills = Bill.objects.filter(user=user).order_by('-order_date_time')
        serializer = OrderListSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    @transaction.atomic
    def post(self, request):
        sid = transaction.savepoint()
        basket_set = request.data.get('cart_item_pk')

        serializer = OrderCreateSerializer(
            data={
                **request.data,
                'basket_set': basket_set
            },
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            bill = get_object_or_404(Bill, pk=serializer.data.get('pk'))
            data = OrderListSerializer(bill).data
            transaction.savepoint_commit(sid)

            return Response(data=data, status=status.HTTP_200_OK)

        transaction.savepoint_rollback(sid)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 주문 조회
class OrderRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )
    queryset = Bill.objects.all()
    serializer_class = OrderListSerializer
