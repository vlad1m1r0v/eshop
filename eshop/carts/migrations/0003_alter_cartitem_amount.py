# Generated by Django 4.0.4 on 2022-06-25 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_alter_cart_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='amount',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
