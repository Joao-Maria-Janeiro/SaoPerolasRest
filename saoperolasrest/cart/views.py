from django.shortcuts import render
from .models import Cart, CartProduct, ShippingDetails, Order
from products.models import Product
from django.http import JsonResponse, HttpResponse
import uuid
from django.contrib.auth.models import User


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
            product.quantity += 1
            product.save()
            return True
    return False

def calc_price(cart):
    if(len(cart.products.all()) == 0):
        cart.total_price = 0
        return
    for product in cart.products.all():
        price = int(product.product.price) * (product.quantity)
        cart.total_price += price
    cart.total_price +=  shipping_price

# Create your views here.
def add_to_cart(request, id):
    if(Product.objects.get(id=id).available_quantity > 0):
        user = get_user(request) 
        if user is not False:
            cart = user.cart
            if not product_is_new(cart, id):
                product = CartProduct(product=Product.objects.get(id=id))
                product.save()
                cart.products.add(product)
            cart.total_price = 0
            calc_price(cart)
            cart.save()
        else:
            name = str(uuid.uuid4())
            email = name + "@gmail.com"
            user = User.objects.create_user(name, email, 'johnpassword')
            user.save()
            user.userprofile.anonymous_user = True
            user.userprofile.save()
            if not product_is_new(cart, id):
                product = CartProduct(product=Product.objects.get(id=id))
                product.save()
                cart.products.add(product)
            cart.total_price = 0
            calc_price(cart)
            cart.save()
    return HttpResponse('Success')