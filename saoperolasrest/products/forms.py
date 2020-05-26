from PIL import Image

from django import forms
from django.core.files import File

from .models import Product, ProductType

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile


class ProductForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Product
        fields = ('image', 'x', 'y', 'width', 'height', 'name', 'description', 'available_quantity', 'price', 'product_type')

    def save(self):
        product = super(ProductForm, self).save(commit=False)
        product.product_type = ProductType.objects.all()[0]
        product.save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(product.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)

        buffer = BytesIO()
        resized_image.save(fp=buffer, format='JPEG')
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

        return product