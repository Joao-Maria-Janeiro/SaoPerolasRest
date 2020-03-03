from django.urls import path, include
from . import views 
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('get-token', csrf_exempt(views.login), name="get-token"),
    path('signup', csrf_exempt(views.signup_view), name="signup"),
    path('add-to-favs', csrf_exempt(views.add_to_favourites), name="add_to_favs"),
    path('get-favs', csrf_exempt(views.get_favourites), name="get-favs"),
]
