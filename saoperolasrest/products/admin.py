from django.contrib import admin

# Register your models here.
from .models import Product, BackGroundImage, CoverPhoto, ProductType

from django.contrib import admin           
   

admin.site.register(Product)


# admin.site.register(Product)
admin.site.register(BackGroundImage)

admin.site.register(CoverPhoto)

admin.site.register(ProductType)