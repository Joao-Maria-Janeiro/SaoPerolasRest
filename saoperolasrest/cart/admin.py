from django.contrib import admin
from .models import Cart, ShippingDetails

# Register your models here.
admin.site.register(Cart)
admin.site.register(ShippingDetails)