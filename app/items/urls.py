from django.urls import path, include


urlpatterns_comment = ([
    path('', items_restful_apis.CommentView.as_view()),
])

urlpatterns_members_signup = ([
    path('', members_apis.SiteSignUpAPIView.as_view()),
    path('check-username/', members_apis.SignUpCheckIDView.as_view()),

], 'signup')

urlpatterns_members = ([
    path('user/', members_apis.UserView.as_view()),
    path('signup/', include(urlpatterns_members_signup)),
    path('login/', members_apis.SiteAuthTokenAPIView.as_view()),
    path('social-login/', members_apis.SocialAuthTokenAPIView.as_view()),
    path('like-item/', members_apis.LikeItemListCreateDestroyView.as_view()),
], 'members')

urlpatterns_order = ([
    path('', bill_restful_apis.OrderListCreateView.as_view()),
    path('<int:pk>/', bill_restful_apis.OrderRetrieveAPIView.as_view()),
], 'order')


urlpatterns_cart = ([
    path('', bill_restful_apis.BasketListCreateAPIView.as_view()),
    path('<int:pk>/', bill_restful_apis.BasketRetrieveUpdateDestroyAPIView.as_view()),
], 'cart')

urlpatterns_category = ([
    path('', items_restful_apis.CategoryListAPIView.as_view()),
    path('<int:pk>/', items_restful_apis.CategoryAPIView.as_view()),
], 'categories')

urlpatterns_search = ([
    path('', items_restful_apis.SearchView.as_view()),
], 'search')

urlpatterns_item = ([
    path('<int:pk>/', items_restful_apis.ItemDetailAPIView.as_view())
], 'item')