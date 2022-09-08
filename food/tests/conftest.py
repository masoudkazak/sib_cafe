import random
from ..models import *
import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth.models import User


def user_create():
    return baker.make(User)

def food_create():
    return baker.make(Food)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def fooditem_create():
    fooditem = baker.make(FoodItem, food=food_create(), days=random.randint(0,5))
    return fooditem


@pytest.fixture
def orderitem_create():
    orderitem = baker.make(
        OrderItem,
        food=food_create(),
        user=user_create(),
        status=random.randint(0,4)
        )
    return orderitem


@pytest.fixture
def review_create():
    review = baker.make(
        Review,
        user=user_create(),
        food=food_create(),
        value=random.randint(0,5)
    )
    return review
