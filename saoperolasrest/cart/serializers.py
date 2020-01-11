from rest_framework import serializers
from .models import Cart, CartProduct, Order, ShippingDetails
from products.serializers import ProductSerializer

class CartProductSerializer(serializers.ModelSerializer):
    productz = ProductSerializer(source='product')
    class Meta:
        model = CartProduct
        fields = ('id', 'productz', 'quantity')

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True)
    class Meta:
        model = Cart
        fields = ('id', 'products', 'total_price')

class OderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ShippingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = '__all__'