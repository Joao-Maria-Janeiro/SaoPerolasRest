from django.shortcuts import render
from .models import Product, BackGroundImage, CoverPhoto, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer, CoverPhotoSerializer, BackGroundImageSerializer
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse, HttpResponse
import json

def get_cover_photos(request):
    queryset = CoverPhoto.objects.order_by('id')
    serializer = CoverPhotoSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_background_photo(request):
    try:
        serialzer = BackGroundImageSerializer(BackGroundImage.objects.all(), many=True)
        return JsonResponse(serialzer.data, safe=False)
    except:
        return HttpResponse("No Background")
    
def get_products(request, p_type):
    try:
        queryset = Product.objects.filter(product_type = ProductType.objects.get(name=p_type))
    except:
        return HttpResponse("There are no products of that type")
    serializer = ProductSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_types(request):
    queryset = ProductType.objects.order_by('id')
    serializer = ProductTypeSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def create_product(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    product = Product(
        name = body['name'],
        description = body['description'],
        price = body['price'],
        image = body['image'],
        product_type = ProductType.objects.get(name = body['type']),
        available_quantity = body['available_quantity'],
    )
    product.save()
    return HttpResponse("Created successfully")