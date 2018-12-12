from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase

from .apis import CategoryItemListAPIView


class CategoryTests(APITestCase):

    total_categories = APIRequestFactory()

    request = total_categories.get('categories/')

    view = CategoryItemListAPIView.as_view()

    response = view(request)