from django.urls import path, include

from items import restful_apis as items_restful_apis
from bill import restful_apis as bill_restful_apis


urlpatterns_cart = ([
    path('', bill_restful_apis.BasketListCreateAPIView.as_view()),
    path('<int:pk>/', bill_restful_apis.BasketUpdateDeleteAPIView.as_view()),
], 'cart')

urlpatterns_category = ([
    path('', items_restful_apis.CategoryListAPIView.as_view()),
    path('<int:pk>/', items_restful_apis.CategoryAPIView.as_view()),
], 'categories')

urlpatterns_restful = ([
    path('categories/', include(urlpatterns_category)),
    path('item/<int:pk>/', items_restful_apis.ItemDetailAPIView.as_view()),
    path('cart/', include(urlpatterns_cart)),
], 'restful')

