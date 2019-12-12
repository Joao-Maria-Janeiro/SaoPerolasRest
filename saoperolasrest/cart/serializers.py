from rest_framework import serializers
from .models import Cart, CartProduct, Order, ShippingDetails

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'

class OderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ShippingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = '__all__'