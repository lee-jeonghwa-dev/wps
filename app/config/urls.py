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


urlpatterns_api_item = ([
    path('', items_apis.ItemDetail.as_view()),
], 'item')


urlpatterns_api_categories = ([
    path('', items_apis.CategoryItemList.as_view()),
], 'categories')

urlpatterns_api = ([
    path('categories/', include(urlpatterns_api_categories)),
    path('item/', include(urlpatterns_api_item)),
], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatterns_api)),
]
