from rest_framework import serializers
from cart.models import ShippingDetails

class ShippingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = '__all__'


