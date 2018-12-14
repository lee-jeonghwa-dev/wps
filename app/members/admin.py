from django.contrib import admin

from .models import User, LikeItem

admin.site.register(User)
admin.site.register(LikeItem)
