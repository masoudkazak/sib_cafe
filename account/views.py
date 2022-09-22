from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.generic import ListView

from .serializers import UserRegisterSerializer, LoginSerializer
from food.models import OrderItem
from .mixins import SuperuserRequiredMixin, IsOwnerOrSuperuser


class UserRegisterAPIView(CreateAPIView):
    queryset = User
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class UserLogoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class DebtListView(SuperuserRequiredMixin, ListView):
    orders_id = OrderItem.objects.filter(status=4).values_list("user", flat=True)
    queryset = User.objects.filter(pk__in=list(orders_id))
    template_name = "account/debts.html"
    context_object_name = "users"


class DebtDetailView(IsOwnerOrSuperuser, ListView):
    template_name = "account/mydebts.html"
    context_object_name = "mydebts"
    
    def get_queryset(self):
        queryset = OrderItem.objects.filter(status=4,
                                            user__username=self.kwargs["username"])
        return queryset
