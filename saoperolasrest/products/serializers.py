from rest_framework import serializers
from .models import Product, ProductType, BackGroundImage, CoverPhoto

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class BackGroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackGroundImage
        fields = '__all__'

class CoverPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPhoto
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'