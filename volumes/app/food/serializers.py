import re
from rest_framework import serializers
from .models import *
from django.core.cache import cache
import datetime
from django.db.models import Sum


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
    rate_avg = serializers.SerializerMethodField("get_avg_rate")

    class Meta:
        model = FoodItem
        fields = ("food", "amount", "rate_avg")
    
    def get_avg_rate(self, obj):
        if not obj.food.is_limit:
            return "Can not rating"

        key = obj.food.title
        if cache.get(key) is None:
            total_value = Review.objects.filter(food=obj.food).aggregate(Sum("value"))["value__sum"]
            cache.set(key, total_value)

        if not cache.get(key):
            return 0
            
        count = Review.objects.filter(food=obj.food).count() 
        return cache.get(key)/count


class OrderCreateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[(0, "Order")])
    class Meta:
        model = OrderItem
        fields = ("food", "status", "user")
    
    def validate_food(self, value):
        today = datetime.date.today().weekday()
        fooditem = FoodItem.objects.get(food=value)

        if fooditem.days != today and fooditem.days != 7:
            raise serializers.ValidationError("Not Today")
        if not fooditem.amount and fooditem.food.is_limit:
            raise serializers.ValidationError("Finished")

        return value
    
    def validate_status(self, value):
        if value != 0:
            raise serializers.ValidationError("")
        return value

    def create(self, validated_data):
        order_food = OrderItem.objects.filter(user=validated_data["user"], status=0, food__is_limit=True)

        if order_food.exists() and validated_data["food"].is_limit:
            fooditem = FoodItem.objects.get(food=order_food[0].food)
            fooditem.amount += 1
            fooditem.save()
            order_food[0].delete()

        if validated_data["food"].is_limit:
            new_fooditem = FoodItem.objects.get(food=validated_data["food"])
            new_fooditem.amount -= 1
            new_fooditem.save()

        order = OrderItem(
            user=validated_data["user"],
            food=validated_data["food"],
            status=validated_data["status"],
            real_price=validated_data["food"].price
        )
        order.save()
        return order


class OrderCancelSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[(1, "Cancel")])

    class Meta:
        model = OrderItem
        fields = ("status", "food")
    
    def validate_status(self, value):
        if value != 1:
            raise serializers.ValidationError()
        return value
    
    def update(self, instance, validated_data):
        fooditem = FoodItem.objects.get(food=validated_data["food"])
        if fooditem.food.is_limit:
            fooditem.amount += 1
            fooditem.save()
        return super().update(instance, validated_data)
        

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("food", "status", "real_price", "created")


class ReviewCreateSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.filter(is_limit=True))
    class Meta:
        model = Review
        fields = ("user", "food", "value")
    
    def validate_value(self, value):
        if value > 5 or value < 0:
            raise serializers.ValidationError()
        return value
    
    def validate_food(self, value):
        if not value.is_limit:
            raise serializers.ValidationError()
        return value
    
    def create(self, validated_data):
        try:
            my_review = Review.objects.get(
                user=validated_data["user"],
                food=validated_data["food"]
                )
        except Review.DoesNotExist:
            pass
        else:
            my_review.delete()
        review = Review(
            user=validated_data["user"],
            food=validated_data["food"],
            value=validated_data["value"]
        )
        review.save()
        return review


class FoodReviewSerializer(serializers.ModelSerializer):
    avg_rate = serializers.SerializerMethodField("get_avg_rate")
    class Meta:
        model = Food
        fields = ("title", "avg_rate")
    
    def get_avg_rate(self, obj):
        key = obj.title
        if cache.get(key) is None:
            total_value = Review.objects.filter(food=obj).aggregate(Sum("value"))["value__sum"]
            cache.set(key, total_value)

        if not cache.get(key):
            return 0

        count = Review.objects.filter(food=obj).count() 
        return cache.get(key)/count
