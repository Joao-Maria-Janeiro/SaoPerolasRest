from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('add/', csrf_exempt(views.add_to_cart), name="add_to_cart"),
    path('get/', views.get_user_cart, name="get_user_cart"),
    path('product/update/', csrf_exempt(views.update_product_quantity_in_cart), name="update_product_quantity_in_cart"),
    path('create-intent/', csrf_exempt(views.createIntent), name="createIntent"),
    path('complete-order/', csrf_exempt(views.complete_order), name="complete_order"),
]
