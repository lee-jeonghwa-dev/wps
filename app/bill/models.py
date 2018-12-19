from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item

User = get_user_model()


# 장바구니에 들어있는 item
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
    # 주문 여부
    order_yn = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}/{self.item.item_name}/{self.amount}'


# 주문
class Bill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    order_date_time = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    delivery_date = models.DateField()
    total_price = models.PositiveIntegerField()

    class Meta:
        ordering = ['-order_date_time']

    def __str__(self):
        return f'{self.user.username}/{self.order_date_time}'
