# Generated by Django 2.1.2 on 2019-12-22 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20191124_2251'),
        ('cart', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous_user', models.BooleanField(default=False)),
                ('use_saved_shipping', models.BooleanField(default=False)),
                ('favourite_products', models.ManyToManyField(blank=True, to='products.Product')),
                ('saved_shipping', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cart.ShippingDetails')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]