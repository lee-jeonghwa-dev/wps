from django.contrib.auth.models import AbstractUser
from django.db import models

from items.models import Item


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    # 사이트에서 회원가입을 한 회원(True)/소셜로그인이용(False)
    site_member = models.BooleanField(default=True)


# 찜하기 (user와 item의 쌍으로 이루어지는 table, 찜해제시 삭제)
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
