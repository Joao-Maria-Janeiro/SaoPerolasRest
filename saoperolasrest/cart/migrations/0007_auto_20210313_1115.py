# Generated by Django 2.1.2 on 2021-03-13 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_coupons_carts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='carts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart'),
        ),
    ]
