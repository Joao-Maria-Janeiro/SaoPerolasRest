from django.urls import path
from . import views

urlpatterns = [
    path('cover-photos/', views.get_cover_photos, name="get_cover_photos"),
]
