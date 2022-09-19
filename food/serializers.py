from rest_framework import serializers
from .models import *
from django.core.cache import cache
import datetime


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
    avg_rate = serializers.SerializerMethodField("get_avg_rate")

    class Meta:
        model = FoodItem
        fields = ("food", "amount", "avg_rate")
    
    def get_avg_rate(self, obj):
        key = obj.food.title
        if cache.get(key) is None:
            cache.set(key, Review().total_value(obj.food))
        count = Review.objects.filter(food=obj.food).count()
        if not count:
            return 0
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
        if not fooditem.amount:
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
    total_rate = serializers.SerializerMethodField("get_total_rate")
    class Meta:
        model = Food
        fields = ("title", "total_rate")
    
    def get_total_rate(self, obj):
        key = obj.title
        if cache.get(key) is None:
            cache.set(key, Review().total_value(obj))
        count = Review.objects.filter(food=obj).count()
        if not count:
            return 0
        return cache.get(key)/count
    