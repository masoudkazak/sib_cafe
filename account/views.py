from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import UserRegisterForm


class UserRegisterView(CreateView):
    model = User
    template_name = "account/register.html"
    form_class = UserRegisterForm
    success_url = '/accounts/login/'