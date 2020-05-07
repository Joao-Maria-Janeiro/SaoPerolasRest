from django.urls import path, include
from . import views 
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('get-token', csrf_exempt(views.login), name="get-token"),
    path('signup', csrf_exempt(views.signup_view), name="signup"),
    path('add-to-favs', csrf_exempt(views.add_to_favourites), name="add_to_favs"),
    path('remove-from-favs', csrf_exempt(views.remove_from_favourites), name="remove_from_favourites"),
    path('get-favs', csrf_exempt(views.get_favourites), name="get-favs"),
    path('update-infos', csrf_exempt(views.update_user_info), name="update-infos"),
    path('get-details', csrf_exempt(views.get_user_details), name="get-user-details"),
    path('remove-multiple-from-favs', csrf_exempt(views.remove_multiple_from_favourites), name="remove_multiple_from_favourites"),
    path('previous-orders', views.get_previous_orders, name="previous_orders"),
]
