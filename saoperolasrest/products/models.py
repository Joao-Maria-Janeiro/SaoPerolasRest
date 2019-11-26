from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

class ProductType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    price = models.FloatField(max_length=5)
    image = models.ImageField(upload_to='page_image', blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)

    def __str__(self):
        return 'Name: {}, ID: {}'.format(self.name, self.id)


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

pre_delete.connect(model_pre_delete, sender=BackGroundImage)
pre_delete.connect(model_pre_delete, sender=CoverPhoto)
pre_save.connect(model_pre_save, sender=BackGroundImage)
pre_save.connect(model_pre_save, sender=CoverPhoto)