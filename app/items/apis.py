from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item, Category
from .serializers import CategorySerializer, ItemsListSerializer, ItemDetailSerializer


# 메인 화면에 카테고리들의 pk를 보내준다
class CategoryItemListAPIView(APIView):
    def get(self, request, format=None):
        if not request.query_params:
            # query_params가 비어있으면 Category List 보여주기
            categories = Category.objects.order_by('pk')
            return Response(CategorySerializer(categories, many=True).data)

        ###################################################################
        # category subcategory내용과 img, list들 보여주기

        # query_params에서 pk, page 값을 가져옴
        categories_pk = request.query_params.get('category_pk')
        page = request.query_params.get('page')

        # pk로 보내지 않은 경우
        if not categories_pk:
            data = {
                'error': 'parameter를 category_pk로 보내주세요',
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=categories_pk)
        except Category.DoesNotExist:
            data = {
                'error': '존재하지 않는 category입니다',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        sub_cetegories = Category.objects.filter(main_category=category.main_category)

        # pk 기준으로 내림차순으로 items목록 정렬
        # 24개씩 나눌 Paginator객체 생성
        paginator = Paginator(
            Item.objects.filter(categories=category).order_by('pk'),
            24,
        )

        # page 목록 생성
        page_list = []
        for num in paginator.page_range:
            page_list.append(num)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # page변수가 정수가 아니어서 발생한 예외의 경우
            # -> 무조건 첫 페이지를 가져옴
            items = paginator.page(1)
        except EmptyPage:
            # page변수에 해당하는 Page에 내용이 없는 경우
            # -> 무조건 마지막 페이지를 가져옴
            items = paginator.page(paginator.num_pages)

        data = {
            'current_categories': CategorySerializer(category).data,
            'sub_categories': CategorySerializer(sub_cetegories, many=True).data,
            'item_list': ItemsListSerializer(items, many=True).data,
            'page_list': page_list,
        }
        return Response(data, status=status.HTTP_200_OK)


class ItemDetailAPIView(APIView):
    def get(self, request, format=None):
        item_pk = request.query_params.get('item_pk')

        # pk로 보내지 않은 경우
        if not item_pk:
            data = {
                'error': 'parameter를 item_pk로 보내주세요, 또는 parameter를 보내지 않았습니',
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
