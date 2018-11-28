from django.db import models


class Item(models.Model):
    item_name = models.CharField(max_length=150)
    company = models.CharField(max_length=50)
    origin_price = models.IntegerField()
    sale_price = models.IntegerField()
    discount_rate = models.FloatField(default=0.0)
    list_thumbnail = models.ImageField(
        upload_to='Item',
    )

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
    photo = models.ImageField(
        upload_to='Category',
    )

    def __str__(self):
        return f'{self.main_category}/{self.sub_category}'


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )

    PHOTO_TYPE_CHOICES = (
        ('T', 'thumbnail'),
        ('D', 'detail'),
    )

    photo_type = models.CharField(max_length=1, choices=PHOTO_TYPE_CHOICES)
    image_order = models.IntegerField(default=1)

    photo = models.ImageField(
        upload_to='ItemImage',
        max_length=300,
    )



    def __str__(self):
        return f'[{self.item.company}]{self.item.item_name}/{self.photo_type}-{self.image_order}'


class Description(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,

    )
    # 상세페이지에서 짧게 붙는 설명
    added_words = models.CharField(max_length=200, null=True, blank=True)
    point = models.IntegerField(default=0)
    delivery_type = models.CharField(max_length=200)
    receive_day = models.CharField(max_length=100)
    regular_delivery = models.BooleanField(default=False)


    # 상품정보고시 내용
    item_type = models.CharField(max_length=50)
    factory_address = models.TextField()
    dom = models.CharField(max_length=100)
    capacity = models.CharField(max_length=30)
    ingredient = models.TextField()
    allergy_material = models.TextField()
    caution = models.TextField()

    def __str__(self):
        return f'[{self.item.company}]{self.item.item_name}'




