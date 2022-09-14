from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
import datetime
from django.db.models import Q
from .permissions import TimePermission


class Menu(ListAPIView):
    permission_classes = [TimePermission]    
    pagination_class = LimitOffsetPagination
    today = datetime.date.today().weekday()
    queryset = FoodItem.objects.filter(Q(days=today) | Q(days=7))
    serializer_class = FoodItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['food__title']
    ordering_fields = ['food__price']


class MenuItem(RetrieveAPIView):
    permission_classes = [TimePermission]
    serializer_class = FoodItemSerializer
    
    def get_object(self):
        fooditem = get_object_or_404(FoodItem ,food__slug=self.kwargs['slug'])
        return fooditem


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated, TimePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderCancelAPIView(RetrieveUpdateAPIView):
    serializer_class = OrderCancelSerializer
    permission_classes = [IsAuthenticated, TimePermission]

    def get_object(self):
        orderitem = get_object_or_404(OrderItem,
                                      user__username=self.kwargs["username"],
                                      pk=self.kwargs["pk"],
                                      status=0
                                      )
        return orderitem


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['status']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user)


class RateCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Leaderboard(ListAPIView):
    queryset = Food.objects.filter(is_limit=True)
    serializer_class = FoodReviewSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']
