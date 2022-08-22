from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import UserRegisterForm

def home(request):
    return render(request, "account/home.html", {})


class UserCreationView(CreateView):
    model = User
    template_name = "account/register.html"
    form_class = UserRegisterForm
    success_url = '/accounts/login/'