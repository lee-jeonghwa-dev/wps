from django.urls import path, include


from members.urls import urlpatterns_members
from items.urls import urlpatterns_item, urlpatterns_search, urlpatterns_category, urlpatterns_comment
from bill.urls import urlpatterns_order, urlpatterns_cart


urlpatterns_new = ([
    # members.urls
    path('members/', include(urlpatterns_members)),
    # items.urls
    path('categories/', include(urlpatterns_category)),
    path('item/', include(urlpatterns_item)),
    path('comment/', include(urlpatterns_comment)),
    path('search/', include(urlpatterns_search)),
    # bill.urls
    path('cart/', include(urlpatterns_cart)),
    path('order/', include(urlpatterns_order)),
], 'new')

