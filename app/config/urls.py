"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from items import apis as items_apis

# api URL연결
import members

# urlpatterns_api = ([
#     # path('posts/', include(urlpatterns_api_posts)),
#     path('members/', include(members.urls)),
# ], 'api')


urlpatterns_api = ([
    path('categories/', items_apis.CategoryList.as_view()),
    # path('items/<int:categories_pk>/', items_apis.ItemList.as_view()),
], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns_api)),
]
