from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('cover-photos/', csrf_exempt(views.get_cover_photos), name="get_cover_photos"),
    path('background/', csrf_exempt(views.get_background_photo), name="background"),
    path('get/all/', views.get_all_products, name="get-all"),
    path('get/rest/', views.get_all_besides_rectangular_images, name="get_all_besides_rectangular_images"),
    path('get/<str:p_type>/', csrf_exempt(views.get_products), name="get_products"),
    path('types/', csrf_exempt(views.get_types), name="types"),
    path('create/', csrf_exempt(views.create_product), name="create_product"),
    path('details/<int:id>/', csrf_exempt(views.get_product_from_id), name="get_product_from_id"),
    path('is-favourite/<int:id>/', csrf_exempt(views.product_is_fav), name="product_is_fav"),
    path('create-product-backend', views.create_product_backend, name="create_product_backend"),
    path('reduce-image-size', views.reduce_image_size, name="reduce_image_size"),
    path('get-all-csv', views.get_all_products_csv, name="get_all_products_csv")
]
