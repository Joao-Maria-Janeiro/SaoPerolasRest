from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

# Create your views here.

# def signup_view(request):
#     try:
#         user = User.objects.get(email = request.POST['email'])
#         return JSONRenderer({'error': 'Já existe um utilizador com este email'})
#     except Exception as e:
#         name = (str(uuid.uuid4()))[:4]
#         user = User.objects.create_user(((request.POST['email']).split("@"))[0] + name, request.POST['email'], request.POST["password1"])
