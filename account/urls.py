from django.urls import path
from .views import *


app_name = "account"


urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("debts/", DebtListView.as_view(), name="debts"),
    path("debts/<str:username>/", DebtDetailView.as_view(), name="mydebts"),
]
