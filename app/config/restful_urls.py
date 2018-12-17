from django.urls import path, include

from items import restful_apis as items_restful_apis
from items import search_apis as search_apis
from bill import restful_apis as bill_restful_apis
from members import restful_apis as members_apis


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

urlpatterns_new = ([
    path('categories/', include(urlpatterns_category)),
    path('item/<int:pk>/', items_restful_apis.ItemDetailAPIView.as_view()),
    path('cart/', include(urlpatterns_cart)),
    path('order/', include(urlpatterns_order)),
    path('members/', include(urlpatterns_members)),
    path('search/', include(urlpatterns_search)),
    path('comment/', include(urlpatterns_comment)),
], 'restful')

