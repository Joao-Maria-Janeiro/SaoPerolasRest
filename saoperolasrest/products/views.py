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
from .forms import ProductForm
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

rectangular_image_product_type = "Colares Compridos"

def get_cover_photos(request):
    queryset = CoverPhoto.objects.order_by('id')
    serializer = CoverPhotoSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_background_photo(request):
    try:
        serialzer = BackGroundImageSerializer(BackGroundImage.objects.order_by('product_type__name'), many=True)
        return JsonResponse(serialzer.data, safe=False)
    except:
        return HttpResponse("No Background")
    
def get_products(request, p_type):
    try:
        queryset = Product.objects.filter(product_type = ProductType.objects.get(name=p_type.replace('-', ' '))).order_by('-id')
    except:
        return HttpResponse("There are no products of that type")
    serializer = ProductSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_all_products(request):
    try:
        queryset = Product.objects.filter(product_type__name = rectangular_image_product_type).order_by('-id')
    except:
        return HttpResponse("There are no products of that type")
    serializer = ProductSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_all_besides_rectangular_images(request):
    try:
        queryset = Product.objects.exclude(product_type__name = rectangular_image_product_type).order_by('-id')
    except:
        return HttpResponse("There are no products of that type")
    serializer = ProductSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


def get_types(request):
    queryset = ProductType.objects.order_by('name')
    serializer = ProductTypeSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_product_from_id(request, id):
    try:
        queryset = Product.objects.get(id=id)
    except:
        return HttpResponse("No matching product")
    serializer = ProductSerializer(queryset, many=False)
    return JsonResponse(serializer.data, safe=False)

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

def create_product_backend(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponse('Produto criado com sucesso')
        else:
            form = ProductForm()
        return render(request, 'products/create_product.html', {'form': form})
    else:
        return HttpResponse('Tem de ser admin para criar um produto')

def product_is_fav(request, id):
    user = get_user(request)
    if user == False:
        return JsonResponse({'error': 'A sua conta não é reconhecida ou a sua sessão terminou, por favor faça login novamente'})
    for product in user.userprofile.favourite_products.all():
        if(product.id == id):
            return JsonResponse({'isFavourite': True})
    return JsonResponse({'isFavourite': False})

def reduce_image_size(request):
    for product in Product.objects.all():
        image = Image.open(product.image)
        if(len(image.fp.read()) > 500000):
            buffer = BytesIO()
            image.save(fp=buffer, format='JPEG', quality=20, optimize=True)
            pill_image = ContentFile(buffer.getvalue())
            image_name = product.image.name
            product.image.delete()
            temp_image = InMemoryUploadedFile(
                pill_image,       
                None,               
                image_name,           
                'image/jpeg',       
                pill_image.tell,  
                None)
            product.image.save(image_name, temp_image)
            product.save()
            temp_image.close()
    return HttpResponse('Success')


def get_all_products_csv(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            output_csv = 'id,title,description,availability,condition,price,link,image_link,brand,inventory,product_type<br>'
            products = Product.objects.all()
            for product in products:
                output_csv += (str(product.id) + ',' + product.name + ',' + product.description.replace(',', ' ') + ',' 
                + 'in stock' + ',' + 'new' + ',' + str(product.price) + ' EUR,' 
                + 'https://saoperolas.pt/#/products/details/' + str(product.id) + ',' + product.image.url + ',' + 'São Pérolas'  + ',' 
                + str(product.available_quantity) + ',' + product.product_type.name + '<br>')
            
            return HttpResponse(output_csv)

        else:
            return HttpResponse('Tem de ser um GET request')
    else:
        return HttpResponse('Tem de ser admin para ver todos os produtos')



