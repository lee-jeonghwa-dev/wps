from django.db import models


class Item(models.Model):
    item_name = models.CharField(max_length=150)
    company = models.CharField(max_length=50)
    origin_price = models.IntegerField()
    sale_price = models.IntegerField()
    discount_rate = models.FloatField(default=0.0)

    categories = models.ManyToManyField('Category')

    def __str__(self):
        return f'[{self.company}]{self.item_name}/{self.origin_price}'

    # def save(self, *args, **kwargs):
    #     if not self.sale_price:
    #         self.sale_price = self.origin_price
    #
    #     super.save(*args, **kwargs)


class Category(models.Model):
    main_category = models.CharField(max_length=30)
    sub_category = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.main_category}/{self.sub_category}'


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        upload_to='ItemImage',
    )
    PHOTO_TYPE_CHOICES = (
        ('T', 'thumbnail'),
        ('D', 'detail'),
    )
    photo_type = models.CharField(max_length=1, choices=PHOTO_TYPE_CHOICES)


