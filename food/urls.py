from django.urls import path
from .views import *


urlpatterns = [
    path("menu/", Menu.as_view(), name="menu")
]
