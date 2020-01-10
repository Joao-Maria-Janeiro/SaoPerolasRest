from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('add/', csrf_exempt(views.add_to_cart), name="add_to_cart"),
]
