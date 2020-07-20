from django.shortcuts import render
from .models import Cart, CartProduct, ShippingDetails, Order, ShippingPrice
from products.models import Product
from django.http import JsonResponse, HttpResponse
import uuid
from django.contrib.auth.models import User
import json
from .serializers import CartSerializer
import stripe
from .email import send_mail
from .keys import STRIPE_KEY

stripe.api_key = STRIPE_KEY
shipping_price = (ShippingPrice.objects.all())[0].price

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
                    if (cart_product.quantity < product.available_quantity):
                        cart_product.quantity += 1
                        cart_product.save()
                    else :
                        return JsonResponse({"error":"Not enough quantity"})
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
        for product in cart.products.all():
            if product.product.available_quantity <= 0:
                cart.products.remove(product)
                product.delete()
        cart.total_price = 0   
        calc_price_and_update(cart)
        cart.save()
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
            return JsonResponse({"error":"A sua sessão expirou, por favor faça login de novo"})
        if body['operation'] == 'increase':
            if product.product.available_quantity >= product.quantity + body['quantity']:
                product.quantity += body['quantity']
                product.save()
                cart.total_price += product.product.price
                if cart.total_price == shipping_price:
                    cart.total_price = 0
                cart.save()
                return JsonResponse({"error":""})
            else:
                return JsonResponse({"error":"A quantidade pretendida não está disponível"})
        elif body['operation'] == 'subtract':
            if product.quantity - body['quantity'] > 0 :
                product.quantity -= body['quantity']
                product.save()
                cart.total_price -= product.product.price
                if cart.total_price == shipping_price:
                    cart.total_price = 0
                cart.save()
                return JsonResponse({"error":""})
            elif product.quantity - body['quantity'] == 0:
                user = get_user(request)
                user.cart.products.remove(product)
                cart.total_price -= ((product.quantity) * product.product.price)
                product.delete()
                if cart.total_price == shipping_price:
                    cart.total_price = 0
                cart.save()
                return JsonResponse({"error":"A quantidade tem de ser maior que 0"})
            else:
                return JsonResponse({"error":"A quantidade tem de ser maior que 0"})
        elif body['operation'] == 'remove':
            cart.products.remove(product)
            cart.total_price -= ((product.quantity) * product.product.price)
            product.delete()
            if cart.total_price == shipping_price:
                    cart.total_price = 0
            cart.save()
            return JsonResponse({"error":""})
        else:
            return JsonResponse({"error":"Operação não reconhecida"})
    else:
        return HttpResponse('POST ONLY')

def createIntent(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if ('token' in body):
            try:
                user = User.objects.get(auth_token=body['token'])
            except:
                return JsonResponse({'error': 'A sua sessão expirou ou credenciais erradas, por favor faça login outra vez'})
            try:
                products = {}
                num_of_prods = 0
                for product in user.cart.products.all():
                    products[product.product.name] = product.quantity
                    num_of_prods += 1
                if(num_of_prods == 0):
                    return JsonResponse({'error': 'O seu carrinho está vazio. Adicione pelo menos um produto antes de prosseguir'})
                if(body['use_saved_details']):
                    intent = stripe.PaymentIntent.create(
                        amount=user.cart.total_price * 100,
                        currency='eur',
                        description='produtos',
                        receipt_email=user.email,
                        metadata=products,
                        shipping = {
                            "name": user.userprofile.saved_shipping.first_name + " " + user.userprofile.saved_shipping.last_name,
                            "phone": user.userprofile.saved_shipping.phone_number,
                            "address": {
                                "city": user.userprofile.saved_shipping.city,
                                "country": user.userprofile.saved_shipping.country,
                                "line1": user.userprofile.saved_shipping.adress,
                                "postal_code": user.userprofile.saved_shipping.zip,
                                "state": user.userprofile.saved_shipping.localidade
                            }
                        }
                    )
                else:
                    intent = stripe.PaymentIntent.create(
                        amount=user.cart.total_price * 100,
                        currency='eur',
                        description='produtos',
                        receipt_email=body['email'],
                        metadata=products,
                        shipping = {
                            "name": body['full_name'],
                            "phone": body['cell'],
                            "address": {
                                "city": body['city'],
                                "country": body['country'],
                                "line1": body['address'],
                                "postal_code": body['zip'],
                                "state": body['localidade']
                            }
                        }
                    )
            except:
                return JsonResponse({'error': 'Ocorreu um erro ao criar a sua encomenda, por favor verifique que todos os detalhes de envio estão corretos. Se o erro persistir recarregue a página'})
            secret = str(uuid.uuid4())
            order = Order(cart=user.cart, total_price=user.cart.total_price * 100, payment_intent_client_secret=intent.client_secret, payment_intent_id=intent.id, shipping_details=user.userprofile.saved_shipping, secret_token=secret)
            order.save()
            return JsonResponse({'token': intent.client_secret, 'secret': secret})
        else:
            try:
                products = {}
                num_of_prods = 0
                for product in body['products']:
                    products[product['name']] = product['quantity']
                    num_of_prods += 1
                if(num_of_prods == 0):
                    return JsonResponse({'error': 'O seu carrinho está vazio. Adicione pelo menos um produto antes de prosseguir'})
                
                total_price = 0
                try:
                    database_products = Product.objects.filter(name__in=products.keys())
                    for product in database_products:
                        total_price += (product.price * products[product.name])
                    total_price += shipping_price
                except:
                    return JsonResponse({'error': 'Um dos produtos que escolheu não existe. Por favor tente novamente'})
                    
                intent = stripe.PaymentIntent.create(
                    amount=total_price * 100,
                    currency='eur',
                    description='produtos',
                    receipt_email=body['email'],
                    metadata=products,
                    shipping = {
                        "name": body['full_name'],
                        "phone": body['cell'],
                        "address": {
                            "city": body['city'],
                            "country": body['country'],
                            "line1": body['address'],
                            "postal_code": body['zip'],
                            "state": body['localidade']
                        }
                    }
                )
            except:
                return JsonResponse({'error': 'Ocorreu um erro ao criar a sua encomenda, por favor verifique que todos os detalhes de envio estão corretos. Se o erro persistir recarregue a página'})
            secret = str(uuid.uuid4())
            order = Order(cart=None, total_price=float(body['total_price']) * 100, 
                payment_intent_client_secret=intent.client_secret, payment_intent_id=intent.id, shipping_details=None, secret_token=secret)
            order.save()
            return JsonResponse({'token': intent.client_secret, 'secret': secret})

def complete_order(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        order = Order.objects.get(payment_intent_client_secret=body['token'], secret_token=body['secret'])
        order.complete = True
        order.save()
        if 'user_token' in body:
            user = User.objects.get(auth_token=body['user_token'])
            if user is False:
                return JsonResponse({"error":"A sua sessão expirou, por favor faça login de novo"})
            for product in user.cart.products.all():
                product.delete()
            user.cart.products.clear()
            user.cart.total_price = 0
            user.cart.save()
            user.userprofile.previous_orders.add(order)
            user.userprofile.save()
        
        intent = stripe.PaymentIntent.retrieve(order.payment_intent_id)
        products = Product.objects.filter(name__in=intent.metadata.keys())
        for product in products:
            product.available_quantity -= int(intent.metadata.get(product.name))
            product.save()
        if send_mail(order, shipping_price, products):
            return JsonResponse({'error': ''})
        else:
            return JsonResponse({'error': 'Ocorreu um erro ao enviar o seu comprovativo por email, por favor envie um email para sao.perolas.pt@gmail.com para resolver a situação'})


def get_order_shipping(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        intent = None
        try:
            order = Order.objects.get(payment_intent_client_secret=body['token'], secret_token=body['secret'])
            intent = stripe.PaymentIntent.retrieve(order.payment_intent_id)
        except:
            return JsonResponse({'error': 'Não conseguimos aceder à sua encomenda'})
        return JsonResponse({
            "nome": intent.shipping["name"],
            "morada_1": intent.shipping["address"]["line1"],
            "morada_2": intent.shipping["address"]["state"] + ", " + intent.shipping["address"]["city"] + " "  + intent.shipping["address"]["postal_code"] + " " + intent.shipping["address"]["country"],
        })

def get_order_shipping_and_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        intent = None
        try:
            intent = stripe.PaymentIntent.retrieve(body['id'])
        except:
            return JsonResponse({'error': 'Não conseguimos aceder à sua encomenda'})
        return JsonResponse({
            "nome": intent.shipping["name"],
            "morada_1": intent.shipping["address"]["line1"],
            "morada_2": intent.shipping["address"]["state"] + ", " + intent.shipping["address"]["city"] + " "  + intent.shipping["address"]["postal_code"] + " " + intent.shipping["address"]["country"],
            "products": intent.metadata
        })

def get_shipping_price(request):
    shipping_price = (ShippingPrice.objects.all())[0].price
    return JsonResponse({'price': shipping_price})

