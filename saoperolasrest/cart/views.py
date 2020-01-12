from django.shortcuts import render
from .models import Cart, CartProduct, ShippingDetails, Order
from products.models import Product
from django.http import JsonResponse, HttpResponse
import uuid
from django.contrib.auth.models import User
import json
from .serializers import CartSerializer


shipping_price = 3

def get_user(request):
    try:
        token = str(request.META['HTTP_AUTHORIZATION']).split(' ')[1]
        user = User.objects.get(auth_token=token)
        return user
    except:
        return False

def product_is_new(cart, id):
    for product in cart.products.all():
        if product.product.id == id:
            return False
    return True

def calc_price_and_update(cart):
    if(len(cart.products.all()) == 0):
        cart.total_price = 0
        return
    for product in cart.products.all():
        price = int(product.product.price) * (product.quantity)
        cart.total_price += price
    cart.total_price +=  shipping_price

# Create your views here.
def add_to_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        product = Product.objects.get(id=body['id'])
        if(product.available_quantity > 0):
            user = get_user(request) 
            if user is not False:
                cart = user.cart
                if product_is_new(cart, body['id']):
                    cart_product = CartProduct(product=product)
                    cart_product.save()
                    cart.products.add(cart_product)
                else:
                    cart_product = CartProduct.objects.get(cart=cart, product = product)
                    cart_product.quantity += 1
                    cart_product.save()
                cart.total_price = 0
                calc_price_and_update(cart)
                cart.save()
            else:
                return JsonResponse({"error":"login failed"})
        else:
            return JsonResponse({"error":"Not enough quantity"})
        return JsonResponse({"error":""})
    else:
        return HttpResponse('POST ONLY')

def get_user_cart(request):
    user = get_user(request)
    if user is not False:
        cart = user.cart
        serializer = CartSerializer(cart, many=False)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":"login failed"})

def update_product_quantity_in_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        product = CartProduct.objects.get(id=body['id'])
        user = get_user(request)
        if user is not False:
            cart = user.cart 
        else:
            return JsonResponse({"error":"A sua sessão expirou, por favor fa;a login de novo"})
        if body['operation'] == 'increase':
            if product.product.available_quantity >= product.quantity + body['quantity']:
                product.quantity += body['quantity']
                product.save()
                cart.total_price += product.product.price
                cart.save()
                return JsonResponse({"error":""})
            else:
                return JsonResponse({"error":"A quantidade pretendida não está disponível"})
        elif body['operation'] == 'subtract':
            if product.quantity - body['quantity'] > 0 :
                product.quantity -= body['quantity']
                product.save()
                cart.total_price -= product.product.price
                cart.save()
                return JsonResponse({"error":""})
            elif product.quantity - body['quantity'] == 0:
                user = get_user(request)
                user.cart.products.remove(product)
                calc_price_and_update(cart)
                cart.save()
                return JsonResponse({"error":"A quantidade tem de ser maior que 0"})
            else:
                return JsonResponse({"error":"A quantidade tem de ser maior que 0"})
        else:
            cart.products.remove(product)
            calc_price_and_update(cart)
            cart.save()
            product.delete()
            return JsonResponse({"error":""})
    else:
        return HttpResponse('POST ONLY')