from django.contrib import admin
from .models import Cart, ShippingDetails, Order, ShippingPrice

# Register your models here.
admin.site.register(Cart)
admin.site.register(ShippingDetails)
admin.site.register(Order)
admin.site.register(ShippingPrice)
