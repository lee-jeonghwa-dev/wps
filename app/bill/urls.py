from django.urls import path
from . import new_apis

urlpatterns_order = ([
    path('', new_apis.OrderListCreateView.as_view()),
    path('<int:pk>/', new_apis.OrderRetrieveAPIView.as_view()),
], 'order')


urlpatterns_cart = ([
    path('', new_apis.BasketListCreateAPIView.as_view()),
    path('<int:pk>/', new_apis.BasketRetrieveUpdateDestroyAPIView.as_view()),
], 'cart')
