from django.contrib.auth.models import AbstractUser
from django.db import models

from items.models import Item


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    site_member = models.BooleanField(default=True)


class LikeItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'item'),
        )
