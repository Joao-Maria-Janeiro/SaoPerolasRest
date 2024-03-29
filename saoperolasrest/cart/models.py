from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

User = get_user_model()

# Create your models here.
class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(CartProduct, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=3, default=0)

def post_save_cart_create(sender, instance, created, *args, **kwargs):
    if created:
        Cart.objects.get_or_create(user=instance)

post_save.connect(post_save_cart_create, sender=settings.AUTH_USER_MODEL)

class ShippingDetails(models.Model):
    first_name = models.CharField(max_length = 300)
    last_name = models.CharField(max_length = 300)
    adress = models.CharField(max_length = 300)
    city = models.CharField(max_length = 300)
    localidade = models.CharField(max_length = 300)
    zip = models.CharField(max_length = 300)
    country = models.CharField(max_length = 300)
    phone_number = models.CharField(max_length = 300)
    email = models.EmailField(null=True)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    total_price = models.IntegerField(default=0)
    date_ordered = models.DateTimeField(auto_now=True)
    payment_intent_client_secret = models.CharField(max_length=300)
    payment_intent_id = models.CharField(max_length=300)
    shipping_details = models.ForeignKey(ShippingDetails, on_delete=models.CASCADE, null=True)
    secret_token = models.CharField(max_length=300)
    complete = models.BooleanField(default=False)

class ShippingPrice(models.Model):
    price = models.IntegerField(default=3)


class Coupons(models.Model):
    expiration_date = models.DateTimeField()
    percentage = models.DecimalField(max_digits=4, decimal_places=3)
    code = models.CharField(max_length=300)
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    minimum_value = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return 'Coupon: {}, Date: {}'.format(self.code, self.expiration_date)

