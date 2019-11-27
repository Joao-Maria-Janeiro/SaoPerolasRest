from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('cover-photos/', csrf_exempt(views.get_cover_photos), name="get_cover_photos"),
    path('background/', csrf_exempt(views.get_background_photo), name="background"),
    path('get/<slug:p_type>/', csrf_exempt(views.get_products), name="get_products"),
    path('types/', csrf_exempt(views.get_types), name="types"),
    path('create/', csrf_exempt(views.create_product), name="create_product"),
    path('image-test/', csrf_exempt(views.image_test), name="image-test"),
]
