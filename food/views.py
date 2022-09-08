from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from .models import *
from .serializers import *


class Menu(ListAPIView):
    serializer_class = FoodSerializer
    pagination_class = LimitOffsetPagination
    queryset = Food.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price']
    