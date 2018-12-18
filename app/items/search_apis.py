from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemsSimpleSerializer


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

        items = Item.objects.filter(item_name__contains=search_str).order_by('pk') | \
                Item.objects.filter(company__contains=search_str).order_by('pk') | \
                Item.objects.filter(description__item_type__contains=search_str).order_by('pk')

        page_list = []
        if not is_ios:
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
