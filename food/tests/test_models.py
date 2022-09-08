import pytest

from food.models import *


pytestmark = pytest.mark.django_db


class TestCreateModel:

    def test_food_and_fooditem_create(self, fooditem_create):
        fooditem = fooditem_create
        assert FoodItem.objects.get(pk=1) == fooditem

    def test_orderitem_create(self, orderitem_create):
        orderitem = orderitem_create
        assert OrderItem.objects.get(pk=1) == orderitem
    
    def test_review_create(self, review_create):
        review = review_create
        assert Review.objects.get(pk=1) == review
