from rest_framework import serializers
from .models import *


class FoodSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")
    avg_review = serializers.SerializerMethodField("get_avg_review")

    class Meta:
        model = Food
        fields = ("title", "image", "price", "description", "avg_review")

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
    
    def get_avg_review(self, obj):
        self.avg_review = Review().avg_value_food(obj)
        return self.avg_review
    

class FoodItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    class Meta:
        model = FoodItem
        fields = ("food", )


class OrderCreateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[(0, "Order")])
    class Meta:
        model = OrderItem
        fields = ("food", "status", "user")
    
    def validate_food(self, value):
        today = datetime.date.today().weekday()
        fooditem = FoodItem.objects.get(food=value)
        if fooditem.days != today:
            raise serializers.ValidationError("Not Today")
        return value
    
    def validate_status(self, value):
        if value != 0:
            raise serializers.ValidationError("")
        return value
        
    
    def create(self, validated_data):
        order_food = OrderItem.objects.filter(user=validated_data["user"], status=0, food__is_limit=True)
            
        if order_food.exists() and validated_data["food"].is_limit:
            order_food[0].delete()
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
        

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("food", "status", "real_price", "updated")


class ReviewSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.filter(is_limit=True))
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

