# Generated by Django 4.0.4 on 2022-06-29 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_user_order_user_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 13, 12, 12, 126961)),
        ),
    ]