# Generated by Django 4.0.4 on 2022-06-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
