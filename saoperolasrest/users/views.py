from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import uuid
from cart.models import Cart
from cart.models import ShippingDetails
from cart.views import get_user
from products.models import Product
from products.serializers import ProductSerializer

# Helper methods

def user_exists(email):
    try:
        User.objects.get(email = email)
        return True
    except Exception as e:
        return False

# Views

def signup_view(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if user_exists(body['email']):
        return JsonResponse({'error': 'Já existe um utilizador com este email'})
    name = (str(uuid.uuid4()))[:4]
    user = User.objects.create_user(((body['email']).split("@"))[0] + name, body['email'], body["password1"])
    user.save()
    user.first_name = body['first_name']
    user.last_name = body['last_name']
    user.email = body['email']
    saved_shipping = ShippingDetails(
        full_name = body['first_name'] + " " + body['last_name'], 
        adress = body['address'],
        city = body['city'],
        localidade = body['localidade'],
        zip = body['zip_code'],
        country = body['country'],
        phone_number = body['cell_number'],
        email = body['email'])
    saved_shipping.save()
    user.userprofile.saved_shipping = saved_shipping
    user.save()
    user.userprofile.save()
    return JsonResponse({})

def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        if not user_exists(email):
            return JsonResponse({"error":"login failed"})
        user = User.objects.get(email = email)
        authenticated = authenticate(username=user.username, password=password)
        if authenticated is not None:
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({"token": token[0].key,"username": user.first_name})
        else:
            return JsonResponse({"error":"login failed"})
    else:
        return HttpResponse('POST ONLY')

def add_to_favourites(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = get_user(request)
        if user == False:
            return JsonResponse({'error': 'A sua conta não é reconhecida ou a sua sessão terminou, por favor faça login novamente'})
        try:
            user.userprofile.favourite_products.add(Product.objects.get(id=body['id']))
        except:
            return JsonResponse({'error': 'Problema ao encontrar o produto selecionado'})
        return JsonResponse({'error': 'Problema ao adicionar o produto aos favoritos, por favor tente mais tarde'})


def get_favourites(request):
    user = get_user(request)
    if user == False:
        return JsonResponse({'error': 'A sua conta não é reconhecida ou a sua sessão terminou, por favor faça login novamente'})
    queryset = None
    try:
        queryset = user.userprofile.favourite_products.all()
    except:
        return JsonResponse({'error': 'Erro ao procurar os seus produtos preferidos, por favor recarregue a página'})
    serializer = ProductSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

def update_user_info(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = get_user(request)
        if body['first_name']:
            user.userprofile.name = body['first_name']
        if body['last_name']:
            user.userprofile.last_name = body['last_name']
        if body['country']:
            user.userprofile.country = body['country']
        if body['address']:
            user.userprofile.address = body['address']
        if body['city']:
            user.userprofile.city = body['city']
        if body['zip_code']:
            user.userprofile.zip_code = body['zip_code']
        if body['localidade']:
            user.userprofile.localidade = body['localidade']
        if body['cell_number']:
            user.userprofile.cell_number = body['cell_number']
        if body['email']:
            user.userprofile.email = body['email']
        user.userprofile.save()
        return JsonResponse({'error': ''})

