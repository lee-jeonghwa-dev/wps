# Generated by Django 2.1.3 on 2018-12-07 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_remove_user_login_from_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='site_member',
            field=models.BooleanField(default=True),
        ),
    ]
