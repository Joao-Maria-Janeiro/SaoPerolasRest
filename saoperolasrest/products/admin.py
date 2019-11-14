from django.contrib import admin

# Register your models here.
from .models import Product, BackGroundImage, CoverPhoto, ProductType

from django.contrib import admin           
from image_cropping import ImageCroppingMixin          

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):          
    pass          

admin.site.register(Product, MyModelAdmin)


# admin.site.register(Product)
admin.site.register(BackGroundImage, MyModelAdmin)

admin.site.register(CoverPhoto, MyModelAdmin)

admin.site.register(ProductType)