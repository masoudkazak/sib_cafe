from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

app_name = "account"

urlpatterns = [
    path("", home, name="home"),
    path("login/", LoginView.as_view(template_name="account/login.html"), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", UserCreationView.as_view(), name="register"),
    path("password_change/", PasswordChangeView.as_view(template_name="account/password_change_form.html",
                                                        success_url=reverse_lazy("account:password_change_done")), name="password_change"),
    path("password_change_done/", PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name="password_change_done"),
]