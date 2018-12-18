from django.contrib import admin
from django.urls import path, include

from config import settings
from items import apis as items_apis
from members import apis as members_apis
from bill import apis as cart_apis

from .new_urls import urlpatterns_new

urlpatterns_api_comment = ([
    path('', items_apis.CommentView.as_view()),
], 'comment')

urlpatterns_api_search = ([
    path('', items_apis.SearchView.as_view()),
], 'search')

urlpatterns_api_order = ([
    path('', cart_apis.OrderView.as_view()),
], 'order')

urlpatterns_api_cart = ([
    path('', cart_apis.ListCreateUpdateBasketItemView.as_view()),
], 'cart')

urlpatterns_api_members_signup = ([
    path('', members_apis.SiteSignUpAPIView.as_view()),
    path('check-username/', members_apis.SignUpCheckIDView.as_view()),
], 'signup')


urlpatterns_api_members = ([
    path('user/', members_apis.UserView.as_view()),
    path('signup/', include(urlpatterns_api_members_signup)),
    path('login/', members_apis.SiteAuthTokenAPIView.as_view()),
    path('social-login/', members_apis.SocialAuthTokenAPIView.as_view()),
    path('like-item/', members_apis.LikeItemListCreateDestroyView.as_view()),
], 'members')


urlpatterns_api_item = ([
    path('', items_apis.ItemDetailAPIView.as_view()),
], 'item')

urlpatterns_api_categories = ([
    path('', items_apis.CategoryItemListAPIView.as_view()),
], 'categories')

urlpatterns_api = ([
    path('categories/', include(urlpatterns_api_categories)),
    path('item/', include(urlpatterns_api_item)),
    path('members/', include(urlpatterns_api_members)),
    path('cart/', include(urlpatterns_api_cart)),
    path('order/', include(urlpatterns_api_order)),
    path('search/', include(urlpatterns_api_search)),
    path('comment/', include(urlpatterns_api_comment)),
], 'api')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlpatterns_api)),
    # 좀더 restful한 접근 방식을 적용한 새로운 API
    path('new/', include(urlpatterns_new)),
]

# if settings.dev.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
