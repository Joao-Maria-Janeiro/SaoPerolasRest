from django.shortcuts import render
from .models import Product, BackGroundImage, CoverPhoto
from .serializers import ProductSerializer, ProductTypeSerializer, CoverPhotoSerializer, BackGroundImageSerializer
from rest_framework.renderers import JSONRenderer
 

def get_cover_photos(request):
    covers = CoverPhoto.objects.order_by('id')
    return JSONRenderer().render(CoverPhotoSerializer(covers, many = True).data)
    
    
