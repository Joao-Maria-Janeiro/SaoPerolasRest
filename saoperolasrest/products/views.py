from django.shortcuts import render
from .models import Product, BackGroundImage, CoverPhoto, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer, CoverPhotoSerializer, BackGroundImageSerializer
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse, HttpResponse
import json
import base64
from django.core import files
import tempfile
from django.core.files.base import ContentFile
from cart.views import get_user


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
    if request.method == 'POST':
        user = get_user(request)
        if user == False:
            return JsonResponse({'error': 'A sua conta não é reconhecida ou a sua sessão terminou, por favor faça login novamente'})
        if user.is_superuser:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            
            data = None
            try:
                data = body['image']
                format, imgstr = data.split(';base64,') 
                ext = format.split('/')[-1] 

                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            except:
                return JsonResponse({'error': 'Erro ao carregar a imagem. Carregou no botão "crop"?'})

            try:
                product = Product(
                    name = body['name'],
                    description = body['description'],
                    price = body['price'],
                    image = data,
                    product_type = ProductType.objects.get(name = body['type']),
                    available_quantity = body['quantity'],
                )
                product.save()
            except:
                return JsonResponse({'error': 'Erro ao criar o produto, por favor verifique que todas as informações estão corretas'})
            return JsonResponse({'error': ''})
        else:
            return JsonResponse({'error': 'Tem de ser admin para criar um produto'})

def product_is_fav(request, id):
    user = get_user(request)
    if user == False:
        return JsonResponse({'error': 'A sua conta não é reconhecida ou a sua sessão terminou, por favor faça login novamente'})
    for product in user.userprofile.favourite_products.all():
        if(product.id == id):
            return JsonResponse({'isFavourite': True})
    return JsonResponse({'isFavourite': False})