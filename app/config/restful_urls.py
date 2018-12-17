from django.urls import path, include

from items import restful_apis as items_restful_apis
from bill import restful_apis as bill_restful_apis

urlpatterns_order = ([
    path('', bill_restful_apis.OrderListCreateView.as_view()),
    path('<int:pk>/', bill_restful_apis.OrderRetrieveAPIView.as_view()),
], 'order')


urlpatterns_cart = ([
    path('', bill_restful_apis.BasketListCreateAPIView.as_view()),
    path('item/<int:item_pk>/', bill_restful_apis.BasketUpdateAPIView.as_view()),
    path('<int:pk>/', bill_restful_apis.BasketUpdateDeleteAPIView.as_view()),
], 'cart')

urlpatterns_category = ([
    path('', items_restful_apis.CategoryListAPIView.as_view()),
    path('<int:pk>/', items_restful_apis.CategoryAPIView.as_view()),
], 'categories')

urlpatterns_new = ([
    path('categories/', include(urlpatterns_category)),
    path('item/<int:pk>', items_restful_apis.ItemDetailAPIView.as_view()),
    path('cart/', include(urlpatterns_cart)),
    path('order/', include(urlpatterns_order)),
], 'restful')

