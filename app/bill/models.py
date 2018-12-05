from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item

User = get_user_model()


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        'Bill',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    amount = models.PositiveSmallIntegerField(default=0)
    order_yn = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}/{self.item.item_name}/{self.amount}'


class Bill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    order_date_time = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    delivery_date = models.DateField(null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-order_date_time']

    def __str__(self):
        return f'{self.user.username}/{self.order_date_time}'
