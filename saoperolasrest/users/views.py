from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import uuid


# Create your views here.

def user_already_exists(request):
    try:
        User.objects.get(email = request.POST['email'])
        return True
    except e:
        return False

def signup_view(request):
    if user_already_exists(request):
        return JSONRenderer({'error': 'Já existe um utilizador com este email'})
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    name = (str(uuid.uuid4()))[:4]
    user = User.objects.create_user(((request.POST['email']).split("@"))[0] + name, request.POST['email'], request.POST["password1"])
    user.save()
    user.cart = Cart(id=0, total_price=0, user=user)
    user.userprofile.name = request.POST['first_name']
    user.userprofile.last_name = request.POST['last_name']
    user.userprofile.country = request.POST['country']
    user.userprofile.address = request.POST['address']
    user.userprofile.city = request.POST['city']
    user.userprofile.zip_code = request.POST['zip_code']
    user.userprofile.localidade = request.POST['localidade']
    user.userprofile.cell_number = request.POST['cell_number']
    user.userprofile.email = request.POST['email']
    user.save()
    user.userprofile.save()
    return JSONRenderer({'error': ''})



def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return HttpResponse('null')
        authenticated = authenticate(username=user.username, password=password)
        if authenticated is not None:
            return HttpResponse(Token.objects.get_or_create(user=user))
        else:
            return HttpResponse('null')
    else:
        return HttpResponse('POST ONLY')