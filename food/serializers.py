from rest_framework import serializers
from .models import *


class FoodSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = Food
        fields = ("title", "image", "price", "description")

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url


class FoodItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    class Meta:
        model = FoodItem
        fields = ("food", "days")


class OrderCreateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[(0, "Order")])
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.filter(pk__in=FoodItem().daily_food_ids()))

    class Meta:
        model = OrderItem
        fields = ("food", "status", "user")
    
    def create(self, validated_data):
        order_food = OrderItem.objects.filter(user=validated_data["user"], status=0, food__is_limit=True)
        
        if order_food.exists() and validated_data["food"].is_limit:
            order_food[0].delete()
        order = OrderItem(
            user=validated_data["user"],
            food=validated_data["food"],
            status=validated_data["status"],
        )
        order.save()
        return order


class OrderCancelSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[(1, "Cancel")])
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.filter(pk__in=FoodItem().daily_food_ids()))

    class Meta:
        model = OrderItem
        fields = ("food", "status")


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("food", "status", "updated")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("user", "food", "value")
    
    def create(self, validated_data):
        try:
            my_review = Review.objects.get(
                user=validated_data['user'],
                food=validated_data["food"]
                )
        except Review.DoesNotExist:
            pass
        else:
            my_review.delete()        
        review = Review(**validated_data)
        review.save()
        return review


class FoodReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )
    class Meta:
        model = Food
        fields = ("title", "reviews")

