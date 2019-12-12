from django.shortcuts import render
from .models import Product, BackGroundImage, CoverPhoto, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer, CoverPhotoSerializer, BackGroundImageSerializer
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse, HttpResponse
import json
import base64
from django.core import files
import tempfile


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

def get_product_from_id(request, id):
    try:
        queryset = Product.objects.get(id=id)
    except:
        return HttpResponse("No matching product")
    serializer = ProductSerializer(queryset, many=False)
    return JsonResponse(serializer.data, safe=False)

## Still under development under here

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

def image_test(request):
    # body_unicode = request.body.decode('utf-8')
    # body = json.loads(request)
    # product = Product(
    #     name = "teste",
    #     description = "dasdasdas",
    #     price = 0,
    #     image = base64.urlsafe_b64decode(request.body),
    #     product_type = ProductType.objects.get(name = "pulseiras"),
    #     available_quantity = 0,
    # )
    # product.save()
    
    lf = tempfile.NamedTemporaryFile()

    lf.write(base64.b64decode(request.body))

    product = Product(
        name = "teste",
        description = "dasdasdas",
        price = 0,
        # image = base64.urlsafe_b64decode(request.body),
        product_type = ProductType.objects.get(name = "pulseiras"),
        available_quantity = 0,
    )
    product.save()
    # Save the temporary image to the model#
    # This saves the model so be sure that is it valid
    product.image.save("test.png", files.File(lf))
    return HttpResponse(request.body)