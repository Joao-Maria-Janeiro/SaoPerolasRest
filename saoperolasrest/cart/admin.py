from django.contrib import admin
from .models import Cart, ShippingDetails, Order

# Register your models here.
admin.site.register(Cart)
admin.site.register(ShippingDetails)
admin.site.register(Order)