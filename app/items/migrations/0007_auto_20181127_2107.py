# Generated by Django 2.1.3 on 2018-11-27 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20181127_1713'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='category',
            index_together={('main_category', 'sub_category')},
        ),
    ]