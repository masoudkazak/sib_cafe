from django.urls import path
from .views import *


app_name = "food"

urlpatterns = [
    path("menu/", Menu.as_view(), name="menu"),
    path("menu/<slug:slug>/", MenuItem.as_view(), name="menuitem"),
    path("order/create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("orders/", OrderListAPIView.as_view(), name="orders"),
    path("add-review/", RateCreateAPIView.as_view(), name="add-review"),
    path("reviews/", Leaderboard.as_view(), name="reviews"),
    path("order/<int:pk>/<str:username>/", OrderCancelAPIView.as_view(), name="order-cancel"),
]
