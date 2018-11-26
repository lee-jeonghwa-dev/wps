from django.contrib import admin

from .models import Item, Category, ItemImage, Description

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(ItemImage)
admin.site.register(Description)
