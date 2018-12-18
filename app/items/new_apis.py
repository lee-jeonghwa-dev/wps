from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item, Category, Comment
from .new_serializers import CategorySerializer, ItemsSimpleSerializer, ItemDetailSerializer, CommentSerializer


# 전체 category 보여주기
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(pk__lt=57)
    serializer_class = CategorySerializer


# 각 카테고리에 속한 item list를 보여준다
class CategoryAPIView(APIView):
    def get(self, request, pk, format=None):
        # query_params에서 page 값을 가져옴
        page = request.query_params.get('page')
        is_ios = request.query_params.get('is_ios')

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            data = {
                'error': '존재하지 않는 category입니다',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        sub_cetegories = Category.objects.filter(main_category=category.main_category)
        page_list = []

        # ios여부 체크 후 ios일 경우 페이징을 적용하지 않음
        if is_ios == 'true':
            items = Item.objects.filter(categories=category).order_by('pk')
        else:
            # pk 기준으로 내림차순으로 items목록 정렬
            # 24개씩 나눌 Paginator객체 생성
            paginator = Paginator(
                Item.objects.filter(categories=category).order_by('pk'),
                24,
            )

            # page 목록 생성
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
            'item_list': ItemsSimpleSerializer(items, many=True).data,
            'page_list': page_list,
            'page': page,
        }
        return Response(data, status=status.HTTP_200_OK)


class ItemDetailAPIView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class CommentView(APIView):
    def post(self, request):
        nickname = request.data.get('nickname')

        if request.auth and not nickname:
            nickname = request.user.username

        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            if nickname:
                serializer.save(nickname=nickname)
            else:
                serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comments = Comment.objects.filter(item__pk=request.data.get('item'))

        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_201_CREATED)


class SearchView(APIView):

    def get(self, request, format=None):
        if not request.query_params:
            data = {
                'error': '검색어를 입력해 주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        search_str = request.query_params.get('search_str')
        page = request.query_params.get('page')
        is_ios = request.query_params.get('is_ios')

        if not search_str:
            data = {
                'error': '검색어를 입력해 주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        items = Item.objects.filter(item_name__contains=search_str) | \
                Item.objects.filter(company__contains=search_str) | \
                Item.objects.filter(description__item_type__contains=search_str)

        page_list = []
        if is_ios == 'true':
            items = items
        else:
            paginator = Paginator(
                items,
                24,
            )

            # page 목록 생성
            for num in paginator.page_range:
                page_list.append(num)

            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)

        data = {
            'items': ItemsSimpleSerializer(items, many=True).data,
            'page_list': page_list,
            'page': page,
        }

        return Response(data, status=status.HTTP_200_OK)
