from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from products.models import Product
from cart.models import ShippingDetails
from django.conf import settings



User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_products = models.ManyToManyField(Product, blank=True)
    anonymous_user = models.BooleanField(default=False)
    use_saved_shipping = models.BooleanField(default=False)
    saved_shipping = models.OneToOneField(ShippingDetails, on_delete=models.CASCADE, null=True)
    # temporary_shipping = models.OneToOneField(ShippingDetails, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)
