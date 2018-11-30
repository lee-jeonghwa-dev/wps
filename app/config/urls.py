from django.contrib import admin
from django.urls import path, include
from items import apis as items_apis
from members import apis as members_apis

urlpatterns_api_members = ([
    path('signup/', members_apis.SiteSignUpAPIView.as_view()),
    path('login/', members_apis.SiteAuthTokenAPIView.as_view()),
    path('social-login/', members_apis.SocialAuthTokenAPIView.as_view()),

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
], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns_api)),
]
