from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import sys

class ProductType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=400, unique=True)
    description = models.TextField()
    price = models.FloatField(max_length=5)
    image = models.ImageField(upload_to='page_image', blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)

    def __str__(self):
        return 'Name: {}, ID: {}'.format(self.name, self.id)
    
    def save(self):
        try:
            im = Image.open(self.image)
            if(len(im.fp.read()) > 500000):
                output = BytesIO()
                im = im.convert('RGB')
                im.save(output, format='JPEG', quality=20, optimize=True)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                                sys.getsizeof(output), None)
        except:
            pass
        super(Product, self).save()



class BackGroundImage(models.Model):
    image = models.ImageField(upload_to='background', blank=True)
    product_type = models.OneToOneField(ProductType, on_delete=models.CASCADE)

class CoverPhoto(models.Model):
    image = models.ImageField(upload_to='cover', blank=True)

def model_pre_delete(sender, instance, *args, **kwargs):
    instance.image.delete()

def model_pre_save(sender, instance, *args, **kwargs):
    try:
        current = None
        if type(instance) == CoverPhoto:
            current = CoverPhoto.objects.get(id=instance.id)
        else :
            current = BackGroundImage.objects.get(id=instance.id)
        if(current.image != instance.image):
            current.image.delete()
    except:
        pass

def product_model_pre_save(sender, instance, *args, **kwargs):
    try:
        current = Product.objects.get(id=instance.id)
        if current.image != instance.image:
            current.image.delete()
    except:
        pass

pre_delete.connect(model_pre_delete, sender=BackGroundImage)
pre_delete.connect(model_pre_delete, sender=CoverPhoto)

pre_save.connect(model_pre_save, sender=BackGroundImage)
pre_save.connect(model_pre_save, sender=CoverPhoto)

pre_delete.connect(model_pre_delete, sender=Product)
pre_save.connect(product_model_pre_save, sender=Product)
