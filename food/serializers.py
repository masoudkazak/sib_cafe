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
        