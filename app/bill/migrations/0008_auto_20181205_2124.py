# Generated by Django 2.1.3 on 2018-12-05 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0007_auto_20181205_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ['-order_date_time']},
        ),
        migrations.AddField(
            model_name='bill',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]