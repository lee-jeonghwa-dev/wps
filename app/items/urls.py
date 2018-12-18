from django.urls import path

from . import new_apis


urlpatterns_comment = ([
    path('', new_apis.CommentView.as_view()),
], 'comment')

urlpatterns_category = ([
    path('', new_apis.CategoryListAPIView.as_view()),
    path('<int:pk>/', new_apis.CategoryAPIView.as_view()),
], 'categories')

urlpatterns_search = ([
    path('', new_apis.SearchView.as_view()),
], 'search')

urlpatterns_item = ([
    path('<int:pk>/', new_apis.ItemDetailAPIView.as_view())
], 'item')
