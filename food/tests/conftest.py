import random
from ..models import *
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from model_bakery import baker


def user_create():
    user = user = User.objects.create_user(
        username="someone",
        password="something"
        )
    return user


def food_create():
    food = Food.objects.create(
        title="chelo",
        price=10000,
        is_limit=True,
        description="dadsadajdooj",
    )
    return food


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def fooditem_create():
    today = datetime.date.today().weekday()
    fooditem = FoodItem.objects.create(
        food=food_create(),
        amount=100,
        days=today
        )
    return fooditem


@pytest.fixture
def orderitem_create():
    orderitem = OrderItem.objects.create(
        food=food_create(),
        user=user_create(),
        status=random.randint(0,4),
        real_price=10000
        )
    return orderitem


@pytest.fixture
def review_create():
    review = Review.objects.create(
        user=user_create(),
        food=food_create(),
        value=random.randint(0,5)
    )
    return review


@pytest.fixture
def user_create_fixture():
    user = user = User.objects.create_user(
        username="someone",
        password="something"
        )
    return user


@pytest.fixture
def food_create_fixture():
    food = Food.objects.create(
        title="chelo",
        price=10000,
        is_limit=True,
        description="dadsadajdooj",
    )

    today = datetime.date.today().weekday()
    FoodItem.objects.create(
        food=food,
        amount=100,
        days=today
        )
    return food


@pytest.fixture
def fooditem_create_bad_days():
    tomorrow = datetime.date.today().weekday() + 1
    fooditem = FoodItem.objects.create(
        food=food_create(),
        amount=100,
        days=tomorrow
        )
    return fooditem


@pytest.fixture
def orderitem_create_for_cancel():
    food = Food.objects.create(
        title="polo",
        price=10000,
        is_limit=True,
        description="dadsadajdooj",
    )
    orderitem = OrderItem.objects.create(
        food=food,
        user=user_create(),
        status=0,
        real_price=10000
        )
    return orderitem


@pytest.fixture
def unlimit_food_create_fixture():
    food = Food.objects.create(
        title="mast",
        price=10000,
        is_limit=False,
        description="dadsadajdooj",
    )
    return food
