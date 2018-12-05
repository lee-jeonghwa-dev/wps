from rest_framework.views import APIView


<<<<<<< Updated upstream
class CreateChangeBasketItem(APIView):
    permission_classes = (

=======
User = get_user_model()


class BasketItemView(APIView):
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
        cart_item_pk = request.data.get('cart_item_pk', 0)
        try:
            cart_item = Basket.objects.get(pk=cart_item_pk, user=user, order_yn=False)
        except Basket.DoesNotExist:
            data = {'error': '존재하지 않는 장바구니 입니다'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        add_amount = request.data.get('add_amount')
        amount = request.data.get('amount')

        if add_amount:
            add_amount = int(add_amount)
        if amount:
            amount = int(amount)

        # 예외사항 check
        if add_amount and amount:
            data = {'error': 'add_amount, amount 모두 있습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if not add_amount and not amount:
            data = {'error': 'add_amount, amount 모두 없습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if cart_item.amount == amount or add_amount == 0:
            data = {'error': 'amount에 변화가 없습니다'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if add_amount:
            if cart_item.amount + add_amount <= 0:
                data = {'error': 'amount가 0 또는 음수입니다'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            cart_item.amount += add_amount

        if amount:
            if amount <= 0:
                data = {'error': 'amount가 0 또는 음수입니다'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            cart_item.amount = amount

        cart_item.save()
        return self.get(request)

    def delete(self, request):
        user = request.user
        cart_item_pk = request.data.get('cart_item_pk', 0)
        try:
            cart_item = Basket.objects.get(pk=cart_item_pk, user=user, order_yn=False)
        except Basket.DoesNotExist:
            data = {'error': '존재하지 않는 장바구니 입니다'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        return self.get(request)


class OrderView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        # IsUser,
>>>>>>> Stashed changes
    )
    def post(self, request):
<<<<<<< Updated upstream
        pass
=======
        user = request.user

        # order=
        a = request.data
        pass
        cart_item_pk_list = request.data.get('cart_item_pk_list')

        pass
        return Response({'test': 'test'})


>>>>>>> Stashed changes

    def put(self, request):
        pass

    def delete(self, request):
         pass