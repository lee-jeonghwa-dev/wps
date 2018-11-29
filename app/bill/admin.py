from django.contrib import admin

from .models import Basket, Bill

admin.site.register(Basket)
admin.site.register(Bill)